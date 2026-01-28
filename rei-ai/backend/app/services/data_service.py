"""
Data Service - Fetch property data from external APIs
"""
import httpx
import logging
from typing import List, Dict, Optional
from ..config import settings

logger = logging.getLogger(__name__)


class DataService:
    """Service for fetching property data from various APIs"""
    
    def __init__(self):
        self.attom_key = settings.ATTOM_API_KEY
        self.realtor_key = settings.REALTOR_API_KEY
        self.use_sample = settings.USE_SAMPLE_DATA
    
    async def get_properties_by_city(self, city: str, state: str = "TX", limit: int = 50) -> List[Dict]:
        """
        Fetch properties for a given city
        Falls back to sample data if API keys not available
        """
        if not self.attom_key or self.use_sample:
            return self._get_sample_properties(city)
        
        try:
            return await self._fetch_from_attom(city, state, limit)
        except Exception as e:
            logger.error(f"Error fetching from ATTOM: {e}")
            return self._get_sample_properties(city)
    
    async def _fetch_from_attom(self, city: str, state: str, limit: int) -> List[Dict]:
        """Fetch from ATTOM Data API"""
        url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/expandedprofile"
        
        headers = {
            "apikey": self.attom_key,
            "accept": "application/json"
        }
        
        params = {
            "address1": city,
            "address2": state,
            "pagesize": limit
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            return self._transform_attom_data(data)
    
    def _transform_attom_data(self, data: Dict) -> List[Dict]:
        """Transform ATTOM API response to our format"""
        properties = []
        
        for prop in data.get("property", []):
            try:
                address = prop.get("address", {})
                building = prop.get("building", {})
                lot = prop.get("lot", {})
                assessment = prop.get("assessment", {})
                
                properties.append({
                    "address": f"{address.get('oneLine', '')}",
                    "city": address.get("locality", ""),
                    "state": address.get("countrySubd", ""),
                    "zip_code": address.get("postal1", ""),
                    "latitude": float(address.get("latitude", 0)),
                    "longitude": float(address.get("longitude", 0)),
                    "property_type": building.get("propertyType", "Single Family"),
                    "bedrooms": int(building.get("rooms", {}).get("beds", 0)),
                    "bathrooms": float(building.get("rooms", {}).get("bathstotal", 0)),
                    "sqft": int(building.get("size", {}).get("bldgsize", 0)),
                    "lot_size": int(lot.get("lotsize1", 0)),
                    "year_built": int(building.get("summary", {}).get("yearbuilt", 0)),
                    "tax_assessment": float(assessment.get("assessed", {}).get("assdttlvalue", 0)),
                    "data_source": "ATTOM"
                })
            except Exception as e:
                logger.error(f"Error transforming property: {e}")
                continue
        
        return properties
    
    def _get_sample_properties(self, city: str) -> List[Dict]:
        """
        Generate sample property data for demonstration
        This allows the app to work without API keys
        """
        import random
        
        # Sample data for Plano, TX
        sample_properties = []
        
        streets = [
            "Park Blvd", "Preston Rd", "Coit Rd", "Independence Pkwy",
            "Spring Creek Pkwy", "Legacy Dr", "Ohio Dr", "Jupiter Rd"
        ]
        
        property_types = ["Single Family", "Townhouse", "Condo"]
        
        # Generate 30 sample properties
        for i in range(30):
            street_num = random.randint(1000, 9999)
            street = random.choice(streets)
            
            bedrooms = random.choice([3, 4, 5])
            bathrooms = random.choice([2, 2.5, 3, 3.5])
            sqft = random.randint(1800, 4500)
            lot_size = random.randint(6000, 12000)
            year_built = random.randint(1990, 2022)
            
            price = sqft * random.randint(180, 320)
            
            sample_properties.append({
                "address": f"{street_num} {street}, {city}, TX",
                "city": city,
                "state": "TX",
                "zip_code": random.choice(["75023", "75024", "75025", "75074", "75075"]),
                "latitude": 33.0198 + random.uniform(-0.05, 0.05),
                "longitude": -96.6989 + random.uniform(-0.05, 0.05),
                "property_type": random.choice(property_types),
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "sqft": sqft,
                "lot_size": lot_size,
                "year_built": year_built,
                "list_price": price,
                "price_per_sqft": round(price / sqft, 2),
                "tax_assessment": price * 0.85,
                "days_on_market": random.randint(1, 90),
                "status": random.choice(["Active", "Active", "Active", "Pending"]),
                "features": {
                    "pool": random.choice([True, False]),
                    "garage": random.randint(2, 3),
                    "fireplace": random.choice([True, False]),
                    "updated_kitchen": random.choice([True, False]),
                    "hardwood_floors": random.choice([True, False])
                },
                "data_source": "SAMPLE"
            })
        
        return sample_properties
    
    async def get_neighborhood_data(self, city: str, zip_code: str) -> Dict:
        """Get neighborhood statistics"""
        # Sample neighborhood data
        return {
            "median_income": 95000,
            "population": 45000,
            "population_growth": 2.3,
            "school_quality_avg": 8.5,
            "crime_rate": 12.5,
            "housing_supply_rate": 1.2,
            "demand_growth_rate": 3.1
        }
