"""
Property Service - Main service orchestrating property operations
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.functions import ST_DWithin, ST_MakePoint
from ..models.property import Property, StreetStats, NeighborhoodStats
from .data_service import DataService
from .analytics_service import AnalyticsService
from .ai_service import AIService
import logging

logger = logging.getLogger(__name__)


class PropertyService:
    """Main service for property operations"""
    
    def __init__(self):
        self.data_service = DataService()
        self.analytics_service = AnalyticsService()
        self.ai_service = AIService()
    
    async def sync_properties(self, db: Session, city: str, state: str = "TX") -> int:
        """
        Fetch properties from external APIs and sync to database
        Returns count of properties synced
        """
        # Fetch from API
        properties_data = await self.data_service.get_properties_by_city(city, state)
        
        count = 0
        for prop_data in properties_data:
            try:
                # Check if property exists
                existing = db.query(Property).filter(
                    Property.address == prop_data['address']
                ).first()
                
                if existing:
                    # Update existing
                    for key, value in prop_data.items():
                        setattr(existing, key, value)
                else:
                    # Create new
                    # Calculate scores
                    scores = self.analytics_service.calculate_property_scores(prop_data)
                    prop_data.update(scores)
                    
                    property_obj = Property(**prop_data)
                    db.add(property_obj)
                
                count += 1
            except Exception as e:
                logger.error(f"Error syncing property {prop_data.get('address')}: {e}")
                continue
        
        db.commit()
        return count
    
    def get_properties(
        self,
        db: Session,
        city: Optional[str] = None,
        zip_code: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_beds: Optional[int] = None,
        max_beds: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Property]:
        """Get properties with filters"""
        query = db.query(Property)
        
        if city:
            query = query.filter(Property.city == city)
        if zip_code:
            query = query.filter(Property.zip_code == zip_code)
        if min_price:
            query = query.filter(Property.list_price >= min_price)
        if max_price:
            query = query.filter(Property.list_price <= max_price)
        if min_beds:
            query = query.filter(Property.bedrooms >= min_beds)
        if max_beds:
            query = query.filter(Property.bedrooms <= max_beds)
        
        return query.offset(skip).limit(limit).all()
    
    def get_property_by_id(self, db: Session, property_id: int) -> Optional[Property]:
        """Get single property by ID"""
        return db.query(Property).filter(Property.id == property_id).first()
    
    def get_nearby_properties(
        self,
        db: Session,
        latitude: float,
        longitude: float,
        radius_miles: float = 0.5
    ) -> List[Property]:
        """
        Get properties within radius of a location
        radius_miles: search radius in miles
        """
        # Convert miles to meters (1 mile = 1609.34 meters)
        radius_meters = radius_miles * 1609.34
        
        point = ST_MakePoint(longitude, latitude)
        
        return db.query(Property).filter(
            ST_DWithin(
                Property.location,
                point,
                radius_meters
            )
        ).all()
    
    async def get_property_analysis(self, db: Session, property_id: int) -> Dict:
        """
        Get comprehensive analysis for a property
        """
        property_obj = self.get_property_by_id(db, property_id)
        if not property_obj:
            return {}
        
        # Convert to dict
        property_data = {
            "id": property_obj.id,
            "address": property_obj.address,
            "city": property_obj.city,
            "state": property_obj.state,
            "zip_code": property_obj.zip_code,
            "latitude": property_obj.latitude,
            "longitude": property_obj.longitude,
            "property_type": property_obj.property_type,
            "bedrooms": property_obj.bedrooms,
            "bathrooms": property_obj.bathrooms,
            "sqft": property_obj.sqft,
            "lot_size": property_obj.lot_size,
            "year_built": property_obj.year_built,
            "list_price": property_obj.list_price,
            "price_per_sqft": property_obj.price_per_sqft,
            "days_on_market": property_obj.days_on_market,
            "status": property_obj.status,
            "features": property_obj.features or {},
        }
        
        # Get street stats
        street_name = self._extract_street_name(property_obj.address)
        street_stats = self.analytics_service.calculate_street_stats(
            db, street_name, property_obj.city
        )
        
        # Get neighborhood data
        neighborhood_data = await self.data_service.get_neighborhood_data(
            property_obj.city, property_obj.zip_code
        )
        
        # Calculate scores
        scores = self.analytics_service.calculate_property_scores(property_data, street_stats)
        
        # Street comparison
        comparison = self.analytics_service.compare_to_street(property_data, street_stats)
        
        # AI scores
        ai_scores = self.analytics_service.calculate_ai_scores(
            property_data, street_stats, neighborhood_data
        )
        
        # Get nearby properties for context
        nearby = self.get_nearby_properties(
            db, property_obj.latitude, property_obj.longitude, radius_miles=0.3
        )
        
        return {
            "property": property_data,
            "scores": scores,
            "ai_scores": ai_scores,
            "street_stats": street_stats,
            "street_comparison": comparison,
            "neighborhood": neighborhood_data,
            "nearby_properties": [
                {
                    "id": p.id,
                    "address": p.address,
                    "price": p.list_price,
                    "sqft": p.sqft,
                    "price_per_sqft": p.price_per_sqft
                }
                for p in nearby[:10]
            ]
        }
    
    async def generate_audit(self, db: Session, property_id: int) -> Dict:
        """
        Generate AI investment audit for a property
        """
        # Get full analysis first
        analysis = await self.get_property_analysis(db, property_id)
        
        if not analysis:
            return {}
        
        # Combine all scores for AI
        all_analytics = {
            **analysis.get('scores', {}),
            **analysis.get('ai_scores', {})
        }
        
        # Generate audit
        audit = await self.ai_service.generate_investment_audit(
            analysis['property'],
            analysis.get('street_stats', {}),
            analysis.get('neighborhood', {}),
            all_analytics
        )
        
        return audit
    
    def get_city_statistics(self, db: Session, city: str) -> Dict:
        """Get aggregated statistics for a city"""
        properties = db.query(Property).filter(Property.city == city).all()
        
        if not properties:
            return {}
        
        prices = [p.list_price for p in properties if p.list_price]
        sqfts = [p.sqft for p in properties if p.sqft]
        ppsf = [p.price_per_sqft for p in properties if p.price_per_sqft]
        
        import numpy as np
        
        return {
            "total_properties": len(properties),
            "avg_price": round(np.mean(prices), 2) if prices else 0,
            "median_price": round(np.median(prices), 2) if prices else 0,
            "min_price": min(prices) if prices else 0,
            "max_price": max(prices) if prices else 0,
            "avg_sqft": round(np.mean(sqfts), 2) if sqfts else 0,
            "avg_price_per_sqft": round(np.mean(ppsf), 2) if ppsf else 0,
            "active_listings": len([p for p in properties if p.status == "Active"]),
        }
    
    def _extract_street_name(self, address: str) -> str:
        """Extract street name from full address"""
        # Simple extraction - take everything between number and city
        parts = address.split(',')[0].strip()
        words = parts.split()
        if len(words) > 1:
            # Skip house number, return rest
            return ' '.join(words[1:])
        return parts
