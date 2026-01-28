"""
Database Initialization Script
Run this to create all tables and load sample data
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import engine, Base, SessionLocal
from app.models import Property, StreetStats, NeighborhoodStats
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """Create all database tables"""
    logger.info("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created successfully")
        
        # Load sample data
        load_sample_data()
        
    except Exception as e:
        logger.error(f"✗ Error creating database: {e}")
        raise


def load_sample_data():
    """Load sample data for demo purposes"""
    logger.info("Loading sample data...")
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = db.query(Property).count()
        if existing_count > 0:
            logger.info(f"Database already contains {existing_count} properties. Skipping sample data.")
            return
        
        # Sample properties for Plano, TX
        import random
        
        streets = [
            ("Park Blvd", "75023"),
            ("Preston Rd", "75024"),
            ("Coit Rd", "75075"),
            ("Independence Pkwy", "75025"),
            ("Spring Creek Pkwy", "75024"),
            ("Legacy Dr", "75024"),
            ("Ohio Dr", "75093"),
            ("Jupiter Rd", "75074")
        ]
        
        logger.info("Creating sample properties...")
        
        for i in range(50):
            street, zip_code = random.choice(streets)
            street_num = random.randint(1000, 9999)
            
            bedrooms = random.choice([3, 4, 5])
            bathrooms = random.choice([2, 2.5, 3, 3.5])
            sqft = random.randint(1800, 4500)
            lot_size = random.randint(6000, 12000)
            year_built = random.randint(1990, 2023)
            
            price = sqft * random.randint(180, 320)
            
            property_obj = Property(
                address=f"{street_num} {street}, Plano, TX",
                city="Plano",
                state="TX",
                zip_code=zip_code,
                latitude=33.0198 + random.uniform(-0.05, 0.05),
                longitude=-96.6989 + random.uniform(-0.05, 0.05),
                property_type=random.choice(["Single Family", "Townhouse", "Condo"]),
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                sqft=sqft,
                lot_size=lot_size,
                year_built=year_built,
                list_price=price,
                price_per_sqft=round(price / sqft, 2),
                tax_assessment=price * 0.85,
                days_on_market=random.randint(1, 90),
                status=random.choice(["Active", "Active", "Active", "Pending"]),
                amenity_score=random.uniform(50, 95),
                structural_score=random.uniform(60, 95),
                location_score=random.uniform(65, 95),
                ai_valuation_score=random.uniform(65, 92),
                ai_growth_score=random.uniform(60, 90),
                ai_risk_score=random.uniform(20, 60),
                data_source="SAMPLE"
            )
            
            db.add(property_obj)
        
        db.commit()
        logger.info("✓ Sample data loaded successfully (50 properties)")
        
        # Create sample neighborhood stats
        logger.info("Creating neighborhood statistics...")
        
        neighborhoods = [
            {
                "neighborhood_name": "West Plano",
                "city": "Plano",
                "zip_code": "75024",
                "median_income": 105000,
                "population": 45000,
                "population_growth": 2.5,
                "school_quality_avg": 9.2,
                "crime_rate": 8.5,
                "infrastructure_score": 85,
                "commercial_density": 70,
                "housing_supply_rate": 1.3,
                "rental_saturation": 0.15,
                "demand_growth_rate": 3.2
            },
            {
                "neighborhood_name": "East Plano",
                "city": "Plano",
                "zip_code": "75074",
                "median_income": 92000,
                "population": 38000,
                "population_growth": 1.8,
                "school_quality_avg": 8.7,
                "crime_rate": 12.3,
                "infrastructure_score": 78,
                "commercial_density": 65,
                "housing_supply_rate": 1.5,
                "rental_saturation": 0.18,
                "demand_growth_rate": 2.8
            }
        ]
        
        for nb_data in neighborhoods:
            nb = NeighborhoodStats(**nb_data)
            db.add(nb)
        
        db.commit()
        logger.info("✓ Neighborhood statistics created")
        
    except Exception as e:
        db.rollback()
        logger.error(f"✗ Error loading sample data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("REI-AI Database Initialization")
    print("=" * 60)
    init_database()
    print("=" * 60)
    print("✓ Database setup complete!")
    print("  You can now start the FastAPI server.")
    print("=" * 60)
