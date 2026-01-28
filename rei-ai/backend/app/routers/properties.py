"""
Properties API Router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..services.property_service import PropertyService
from pydantic import BaseModel

router = APIRouter(prefix="/properties", tags=["properties"])
property_service = PropertyService()


# Response Models
class PropertyResponse(BaseModel):
    id: int
    address: str
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float
    property_type: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[float]
    sqft: Optional[int]
    lot_size: Optional[int]
    year_built: Optional[int]
    list_price: Optional[float]
    price_per_sqft: Optional[float]
    days_on_market: Optional[int]
    status: Optional[str]
    amenity_score: Optional[float]
    structural_score: Optional[float]
    location_score: Optional[float]
    ai_valuation_score: Optional[float]
    ai_growth_score: Optional[float]
    ai_risk_score: Optional[float]
    
    class Config:
        from_attributes = True


@router.post("/sync/{city}")
async def sync_properties(
    city: str,
    state: str = "TX",
    db: Session = Depends(get_db)
):
    """
    Sync properties from external APIs to database
    """
    count = await property_service.sync_properties(db, city, state)
    return {
        "message": f"Successfully synced {count} properties for {city}, {state}",
        "count": count
    }


@router.get("/", response_model=List[PropertyResponse])
def get_properties(
    city: Optional[str] = Query(None, description="Filter by city"),
    zip_code: Optional[str] = Query(None, description="Filter by ZIP code"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    min_beds: Optional[int] = Query(None, description="Minimum bedrooms"),
    max_beds: Optional[int] = Query(None, description="Maximum bedrooms"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get properties with optional filters
    """
    properties = property_service.get_properties(
        db=db,
        city=city,
        zip_code=zip_code,
        min_price=min_price,
        max_price=max_price,
        min_beds=min_beds,
        max_beds=max_beds,
        skip=skip,
        limit=limit
    )
    return properties


@router.get("/{property_id}")
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    """
    Get single property by ID
    """
    property_obj = property_service.get_property_by_id(db, property_id)
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_obj


@router.get("/{property_id}/analysis")
async def get_property_analysis(
    property_id: int,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive analysis for a property
    """
    analysis = await property_service.get_property_analysis(db, property_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Property not found")
    return analysis


@router.post("/{property_id}/audit")
async def generate_audit(
    property_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate AI investment audit for a property
    """
    audit = await property_service.generate_audit(db, property_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Property not found")
    return audit


@router.get("/nearby/search")
def get_nearby_properties(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    radius_miles: float = Query(0.5, ge=0.1, le=5, description="Search radius in miles"),
    db: Session = Depends(get_db)
):
    """
    Get properties near a location
    """
    properties = property_service.get_nearby_properties(
        db, latitude, longitude, radius_miles
    )
    return properties


@router.get("/city/{city}/stats")
def get_city_statistics(
    city: str,
    db: Session = Depends(get_db)
):
    """
    Get aggregated statistics for a city
    """
    stats = property_service.get_city_statistics(db, city)
    if not stats:
        raise HTTPException(status_code=404, detail="No properties found for this city")
    return stats
