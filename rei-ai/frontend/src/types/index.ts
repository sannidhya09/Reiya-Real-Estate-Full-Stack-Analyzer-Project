/**
 * TypeScript Type Definitions
 */

export interface Property {
  id: number;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  latitude: number;
  longitude: number;
  property_type?: string;
  bedrooms?: number;
  bathrooms?: number;
  sqft?: number;
  lot_size?: number;
  year_built?: number;
  list_price?: number;
  price_per_sqft?: number;
  days_on_market?: number;
  status?: string;
  features?: Record<string, any>;
  amenity_score?: number;
  structural_score?: number;
  location_score?: number;
  ai_valuation_score?: number;
  ai_growth_score?: number;
  ai_risk_score?: number;
}

export interface StreetStats {
  avg_price: number;
  median_price: number;
  avg_price_per_sqft: number;
  std_price: number;
  avg_sqft: number;
  property_count: number;
}

export interface NeighborhoodData {
  median_income: number;
  population: number;
  population_growth: number;
  school_quality_avg: number;
  crime_rate: number;
  housing_supply_rate: number;
  demand_growth_rate: number;
}

export interface PropertyAnalysis {
  property: Property;
  scores: {
    amenity_score: number;
    structural_score: number;
    location_score: number;
    rental_yield: number;
    appreciation_rate: number;
    demand_index: number;
    supply_index: number;
    volatility_score: number;
  };
  ai_scores: {
    ai_valuation_score: number;
    ai_growth_score: number;
    ai_risk_score: number;
  };
  street_stats: StreetStats;
  street_comparison: {
    price_zscore?: number;
    price_percentile?: number;
    ppsf_ratio?: number;
    ppsf_vs_street?: number;
    sqft_ratio?: number;
  };
  neighborhood: NeighborhoodData;
  nearby_properties: Array<{
    id: number;
    address: string;
    price: number;
    sqft: number;
    price_per_sqft: number;
  }>;
}

export interface AIAudit {
  property_id: number;
  summary: string;
  investment_thesis: string;
  full_report: string;
  overall_score: number;
  valuation_score: number;
  growth_score: number;
  risk_score: number;
  sections?: Record<string, string>;
}

export interface CityStats {
  total_properties: number;
  avg_price: number;
  median_price: number;
  min_price: number;
  max_price: number;
  avg_sqft: number;
  avg_price_per_sqft: number;
  active_listings: number;
}

export interface PropertyFilters {
  city?: string;
  zip_code?: string;
  min_price?: number;
  max_price?: number;
  min_beds?: number;
  max_beds?: number;
}
