"""
Analytics Service - Property analysis and scoring
"""
import numpy as np
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..models.property import Property, StreetStats
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for property analytics and scoring"""
    
    def calculate_property_scores(self, property_data: Dict, street_stats: Optional[Dict] = None) -> Dict:
        """
        Calculate various scores for a property
        Returns: Dictionary with all computed scores
        """
        scores = {}
        
        # Amenity Score (0-100)
        scores['amenity_score'] = self._calculate_amenity_score(property_data.get('features', {}))
        
        # Structural Score (based on age and size)
        scores['structural_score'] = self._calculate_structural_score(
            property_data.get('year_built', 2000),
            property_data.get('sqft', 0)
        )
        
        # Location Score (based on price per sqft relative to area)
        if street_stats:
            scores['location_score'] = self._calculate_location_score(
                property_data.get('price_per_sqft', 0),
                street_stats
            )
        else:
            scores['location_score'] = 75.0  # Default
        
        # Investment Metrics
        scores.update(self._calculate_investment_metrics(property_data))
        
        return scores
    
    def _calculate_amenity_score(self, features: Dict) -> float:
        """
        Calculate amenity score based on property features
        Score: 0-100
        """
        if not features:
            return 50.0
        
        score = 50.0  # Base score
        
        # Add points for each amenity
        amenity_weights = {
            'pool': 10,
            'updated_kitchen': 8,
            'hardwood_floors': 7,
            'fireplace': 5,
            'smart_home': 8,
            'solar_panels': 10,
            'new_hvac': 7,
            'new_roof': 6,
            'finished_basement': 9,
            'garage': 3  # per space
        }
        
        for amenity, weight in amenity_weights.items():
            if amenity in features:
                if amenity == 'garage' and isinstance(features[amenity], int):
                    score += features[amenity] * weight
                elif features[amenity]:
                    score += weight
        
        return min(score, 100.0)
    
    def _calculate_structural_score(self, year_built: int, sqft: int) -> float:
        """
        Calculate structural condition score
        Considers age and size
        """
        from datetime import datetime
        
        current_year = datetime.now().year
        age = current_year - year_built
        
        # Age score (newer is better, but vintage homes can be good too)
        if age < 5:
            age_score = 100
        elif age < 10:
            age_score = 95
        elif age < 20:
            age_score = 85
        elif age < 30:
            age_score = 75
        elif age < 50:
            age_score = 65
        else:
            age_score = 60  # Vintage homes
        
        # Size score (optimal range: 2000-3500 sqft)
        if 2000 <= sqft <= 3500:
            size_score = 100
        elif 1500 <= sqft < 2000:
            size_score = 90
        elif 3500 < sqft <= 4500:
            size_score = 90
        elif sqft < 1500:
            size_score = 70
        else:
            size_score = 75
        
        # Weighted average
        return (age_score * 0.6) + (size_score * 0.4)
    
    def _calculate_location_score(self, price_per_sqft: float, street_stats: Dict) -> float:
        """
        Calculate location score based on price comparison
        """
        avg_ppsf = street_stats.get('avg_price_per_sqft', price_per_sqft)
        
        if avg_ppsf == 0:
            return 75.0
        
        # Calculate ratio
        ratio = price_per_sqft / avg_ppsf
        
        # Score based on how close to average (sweet spot is 0.95-1.05)
        if 0.95 <= ratio <= 1.05:
            score = 100
        elif 0.85 <= ratio < 0.95:
            score = 95  # Slightly undervalued (good for buyers)
        elif 1.05 < ratio <= 1.15:
            score = 90  # Slightly premium
        elif ratio < 0.85:
            score = 80  # Significantly undervalued (check why)
        else:
            score = 70  # Overpriced
        
        return score
    
    def _calculate_investment_metrics(self, property_data: Dict) -> Dict:
        """
        Calculate investment-related metrics
        """
        sqft = property_data.get('sqft', 1)
        price = property_data.get('list_price', 0)
        
        # Rental yield estimate (simplified)
        estimated_rent = sqft * 1.2  # $1.2 per sqft average
        annual_rent = estimated_rent * 12
        rental_yield = (annual_rent / price * 100) if price > 0 else 0
        
        # Appreciation rate (based on age and location quality)
        year_built = property_data.get('year_built', 2000)
        age = 2024 - year_built
        
        if age < 10:
            appreciation_rate = 4.5
        elif age < 20:
            appreciation_rate = 3.8
        else:
            appreciation_rate = 3.2
        
        # Demand index (simplified)
        days_on_market = property_data.get('days_on_market', 30)
        if days_on_market < 15:
            demand_index = 90
        elif days_on_market < 30:
            demand_index = 80
        elif days_on_market < 60:
            demand_index = 70
        else:
            demand_index = 60
        
        return {
            'rental_yield': round(rental_yield, 2),
            'appreciation_rate': round(appreciation_rate, 2),
            'demand_index': demand_index,
            'supply_index': 70,  # Placeholder
            'volatility_score': 25  # Lower is better
        }
    
    def calculate_street_stats(self, db: Session, street_name: str, city: str) -> Dict:
        """
        Calculate aggregated statistics for a street
        """
        properties = db.query(Property).filter(
            Property.address.like(f"%{street_name}%"),
            Property.city == city
        ).all()
        
        if not properties:
            return {}
        
        prices = [p.list_price for p in properties if p.list_price]
        price_per_sqft = [p.price_per_sqft for p in properties if p.price_per_sqft]
        sqfts = [p.sqft for p in properties if p.sqft]
        
        stats = {
            'property_count': len(properties),
            'avg_price': np.mean(prices) if prices else 0,
            'median_price': np.median(prices) if prices else 0,
            'avg_price_per_sqft': np.mean(price_per_sqft) if price_per_sqft else 0,
            'std_price': np.std(prices) if prices else 0,
            'avg_sqft': np.mean(sqfts) if sqfts else 0,
        }
        
        return stats
    
    def compare_to_street(self, property_data: Dict, street_stats: Dict) -> Dict:
        """
        Compare a property to street averages
        Returns percentile ranks and z-scores
        """
        if not street_stats:
            return {}
        
        comparison = {}
        
        # Price comparison
        price = property_data.get('list_price', 0)
        avg_price = street_stats.get('avg_price', 0)
        std_price = street_stats.get('std_price', 1)
        
        if std_price > 0:
            price_zscore = (price - avg_price) / std_price
            comparison['price_zscore'] = round(price_zscore, 2)
            comparison['price_percentile'] = self._zscore_to_percentile(price_zscore)
        
        # Price per sqft comparison
        ppsf = property_data.get('price_per_sqft', 0)
        avg_ppsf = street_stats.get('avg_price_per_sqft', 0)
        
        if avg_ppsf > 0:
            ppsf_ratio = ppsf / avg_ppsf
            comparison['ppsf_ratio'] = round(ppsf_ratio, 2)
            comparison['ppsf_vs_street'] = round((ppsf_ratio - 1) * 100, 1)  # % difference
        
        # Size comparison
        sqft = property_data.get('sqft', 0)
        avg_sqft = street_stats.get('avg_sqft', 0)
        
        if avg_sqft > 0:
            comparison['sqft_ratio'] = round(sqft / avg_sqft, 2)
        
        return comparison
    
    def _zscore_to_percentile(self, zscore: float) -> int:
        """Convert z-score to percentile"""
        from scipy.stats import norm
        return int(norm.cdf(zscore) * 100)
    
    def calculate_ai_scores(self, property_data: Dict, street_stats: Dict, neighborhood_data: Dict) -> Dict:
        """
        Calculate AI-based scores using weighted multi-factor analysis
        """
        # Valuation Score (0-100)
        # Based on price relative to comparable properties
        ppsf_ratio = property_data.get('price_per_sqft', 200) / street_stats.get('avg_price_per_sqft', 200)
        
        if ppsf_ratio < 0.9:
            valuation_score = 90  # Undervalued
        elif ppsf_ratio < 0.95:
            valuation_score = 85
        elif ppsf_ratio <= 1.05:
            valuation_score = 80  # Fair value
        elif ppsf_ratio <= 1.10:
            valuation_score = 70
        else:
            valuation_score = 60  # Overvalued
        
        # Growth Score (0-100)
        # Based on neighborhood trends and property characteristics
        pop_growth = neighborhood_data.get('population_growth', 2.0)
        property_age = 2024 - property_data.get('year_built', 2000)
        
        growth_score = min(70 + (pop_growth * 5) - (property_age * 0.3), 100)
        
        # Risk Score (0-100, lower is better)
        days_on_market = property_data.get('days_on_market', 30)
        crime_rate = neighborhood_data.get('crime_rate', 15)
        
        risk_score = min(50 + (days_on_market * 0.3) + (crime_rate * 0.5), 100)
        
        return {
            'ai_valuation_score': round(valuation_score, 1),
            'ai_growth_score': round(growth_score, 1),
            'ai_risk_score': round(risk_score, 1)
        }
