"""
Database Models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Index
from sqlalchemy.sql import func
from geoalchemy2 import Geography
from ..database import Base


class Property(Base):
    """Property data model with comprehensive attributes"""
    __tablename__ = "properties"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    address = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False, index=True)
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(Geography(geometry_type='POINT', srid=4326))
    
    # Property Details
    property_type = Column(String)  # Single Family, Condo, Townhouse
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    sqft = Column(Integer)
    lot_size = Column(Integer)
    year_built = Column(Integer)
    
    # Pricing
    list_price = Column(Float)
    price_per_sqft = Column(Float)
    tax_assessment = Column(Float)
    estimated_value = Column(Float)
    
    # Market Data
    days_on_market = Column(Integer)
    listing_date = Column(DateTime)
    status = Column(String)  # Active, Pending, Sold
    
    # Features (JSON)
    features = Column(JSON)  # Pool, solar, garage, etc.
    
    # Scores (Computed)
    amenity_score = Column(Float)
    structural_score = Column(Float)
    location_score = Column(Float)
    school_quality_index = Column(Float)
    crime_index = Column(Float)
    accessibility_index = Column(Float)
    
    # Investment Metrics
    rental_yield = Column(Float)
    appreciation_rate = Column(Float)
    volatility_score = Column(Float)
    demand_index = Column(Float)
    supply_index = Column(Float)
    
    # AI Scores
    ai_valuation_score = Column(Float)
    ai_risk_score = Column(Float)
    ai_growth_score = Column(Float)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    data_source = Column(String)
    
    # Indexes
    __table_args__ = (
        Index('idx_location', 'latitude', 'longitude'),
        Index('idx_city_zip', 'city', 'zip_code'),
        Index('idx_price', 'list_price'),
    )


class StreetStats(Base):
    """Aggregated statistics at street level"""
    __tablename__ = "street_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    street_name = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    zip_code = Column(String, nullable=False)
    
    # Aggregated Metrics
    avg_price = Column(Float)
    avg_price_per_sqft = Column(Float)
    avg_sqft = Column(Float)
    avg_lot_size = Column(Float)
    avg_bedrooms = Column(Float)
    avg_bathrooms = Column(Float)
    
    # Statistical Measures
    variance_price = Column(Float)
    std_price = Column(Float)
    median_price = Column(Float)
    
    # Market Dynamics
    turnover_rate = Column(Float)
    renovation_density = Column(Float)
    investor_ratio = Column(Float)
    growth_rate = Column(Float)
    
    # Property Count
    property_count = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class NeighborhoodStats(Base):
    """Neighborhood-level statistics"""
    __tablename__ = "neighborhood_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    neighborhood_name = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    zip_code = Column(String)
    
    # Demographics
    median_income = Column(Float)
    population = Column(Integer)
    population_growth = Column(Float)
    
    # Education
    school_quality_avg = Column(Float)
    school_count = Column(Integer)
    
    # Safety
    crime_rate = Column(Float)
    crime_index = Column(Float)
    
    # Infrastructure
    infrastructure_score = Column(Float)
    commercial_density = Column(Float)
    
    # Housing Market
    housing_supply_rate = Column(Float)
    rental_saturation = Column(Float)
    demand_growth_rate = Column(Float)
    avg_appreciation = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AIAudit(Base):
    """AI-generated audit reports"""
    __tablename__ = "ai_audits"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False, index=True)
    
    # Report Content
    report_json = Column(JSON)  # Full structured report
    summary = Column(String)
    investment_thesis = Column(String)
    
    # Scores
    overall_score = Column(Float)
    valuation_score = Column(Float)
    growth_score = Column(Float)
    risk_score = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
