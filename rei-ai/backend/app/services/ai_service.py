"""
AI Service - Generate investment audit reports using OpenAI
"""
import json
import logging
from typing import Dict, Optional
from openai import AsyncOpenAI
from ..config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered analysis using OpenAI"""
    
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_investment_audit(
        self,
        property_data: Dict,
        street_stats: Dict,
        neighborhood_data: Dict,
        analytics: Dict
    ) -> Dict:
        """
        Generate comprehensive AI-powered investment audit
        """
        if not self.client:
            return self._generate_sample_audit(property_data, analytics)
        
        try:
            # Prepare context for AI
            context = self._prepare_audit_context(
                property_data, street_stats, neighborhood_data, analytics
            )
            
            # Generate audit using GPT-4
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": f"Generate an investment audit for this property:\n\n{json.dumps(context, indent=2)}"
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            audit_text = response.choices[0].message.content
            
            return {
                "property_id": property_data.get("id"),
                "summary": self._extract_summary(audit_text),
                "investment_thesis": self._extract_thesis(audit_text),
                "full_report": audit_text,
                "overall_score": analytics.get('ai_valuation_score', 75),
                "valuation_score": analytics.get('ai_valuation_score', 75),
                "growth_score": analytics.get('ai_growth_score', 70),
                "risk_score": analytics.get('ai_risk_score', 35),
                "sections": self._parse_audit_sections(audit_text)
            }
        
        except Exception as e:
            logger.error(f"Error generating AI audit: {e}")
            return self._generate_sample_audit(property_data, analytics)
    
    def _get_system_prompt(self) -> str:
        """System prompt for investment audit generation"""
        return """You are an expert real estate investment analyst with deep knowledge of:
- Property valuation and comparative market analysis
- Urban economics and neighborhood dynamics
- Investment risk assessment
- Real estate market trends

Generate a professional, data-driven investment audit report with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
2. PROPERTY VALUATION ANALYSIS
   - Current market positioning
   - Price per square foot analysis
   - Comparison to street and neighborhood averages
3. LOCATION & NEIGHBORHOOD ASSESSMENT
   - Neighborhood quality indicators
   - Growth trends and demographics
   - Infrastructure and amenities
4. INVESTMENT METRICS
   - Rental yield potential
   - Appreciation forecast
   - Risk factors
5. STREET-LEVEL COMPARISON
   - How this property compares to nearby homes
   - Market positioning
6. RISK ASSESSMENT
   - Key risk factors
   - Mitigation strategies
7. INVESTMENT THESIS (Final recommendation with confidence level)

Use quantitative data provided. Be specific, analytical, and professional.
Format the report with clear headers and bullet points for readability.
"""
    
    def _prepare_audit_context(
        self,
        property_data: Dict,
        street_stats: Dict,
        neighborhood_data: Dict,
        analytics: Dict
    ) -> Dict:
        """Prepare structured context for AI"""
        return {
            "property": {
                "address": property_data.get("address"),
                "type": property_data.get("property_type"),
                "price": property_data.get("list_price"),
                "price_per_sqft": property_data.get("price_per_sqft"),
                "bedrooms": property_data.get("bedrooms"),
                "bathrooms": property_data.get("bathrooms"),
                "sqft": property_data.get("sqft"),
                "lot_size": property_data.get("lot_size"),
                "year_built": property_data.get("year_built"),
                "features": property_data.get("features", {}),
                "days_on_market": property_data.get("days_on_market")
            },
            "street_stats": street_stats,
            "neighborhood": neighborhood_data,
            "analytics": {
                "amenity_score": analytics.get("amenity_score"),
                "structural_score": analytics.get("structural_score"),
                "location_score": analytics.get("location_score"),
                "valuation_score": analytics.get("ai_valuation_score"),
                "growth_score": analytics.get("ai_growth_score"),
                "risk_score": analytics.get("ai_risk_score"),
                "rental_yield": analytics.get("rental_yield"),
                "appreciation_rate": analytics.get("appreciation_rate"),
                "demand_index": analytics.get("demand_index")
            }
        }
    
    def _extract_summary(self, audit_text: str) -> str:
        """Extract executive summary from audit"""
        lines = audit_text.split('\n')
        summary_lines = []
        in_summary = False
        
        for line in lines:
            if 'EXECUTIVE SUMMARY' in line.upper():
                in_summary = True
                continue
            if in_summary:
                if line.strip() and not line.strip().startswith('#'):
                    summary_lines.append(line.strip())
                if len(summary_lines) >= 3 or (line.strip().startswith('#') and summary_lines):
                    break
        
        return ' '.join(summary_lines) if summary_lines else audit_text[:200]
    
    def _extract_thesis(self, audit_text: str) -> str:
        """Extract investment thesis from audit"""
        lines = audit_text.split('\n')
        thesis_lines = []
        in_thesis = False
        
        for line in lines:
            if 'INVESTMENT THESIS' in line.upper():
                in_thesis = True
                continue
            if in_thesis and line.strip():
                thesis_lines.append(line.strip())
        
        return ' '.join(thesis_lines) if thesis_lines else "Moderate investment opportunity with balanced risk-reward profile."
    
    def _parse_audit_sections(self, audit_text: str) -> Dict:
        """Parse audit into structured sections"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in audit_text.split('\n'):
            if line.strip().startswith('#') or line.strip().isupper():
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip('#').strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _generate_sample_audit(self, property_data: Dict, analytics: Dict) -> Dict:
        """
        Generate a sample audit when OpenAI is not available
        This ensures the app works even without API key
        """
        address = property_data.get("address", "Property")
        price = property_data.get("list_price", 0)
        ppsf = property_data.get("price_per_sqft", 0)
        sqft = property_data.get("sqft", 0)
        
        valuation_score = analytics.get('ai_valuation_score', 75)
        growth_score = analytics.get('ai_growth_score', 70)
        risk_score = analytics.get('ai_risk_score', 35)
        
        report = f"""# INVESTMENT AUDIT REPORT
## {address}

### EXECUTIVE SUMMARY
This property presents a {"strong" if valuation_score > 80 else "moderate"} investment opportunity with a current listing price of ${price:,.0f} (${ppsf}/sqft). The property demonstrates {"above-average" if valuation_score > 75 else "average"} market positioning within its neighborhood, with a valuation score of {valuation_score}/100.

### PROPERTY VALUATION ANALYSIS

**Market Positioning**: {valuation_score}/100
- Current asking price: ${price:,.0f}
- Price per square foot: ${ppsf:.2f}
- Total living area: {sqft:,} sq ft

The property is currently {"competitively" if 75 <= valuation_score <= 85 else "attractively" if valuation_score > 85 else "moderately"} priced relative to comparable properties in the immediate area.

### LOCATION & NEIGHBORHOOD ASSESSMENT

**Growth Score**: {growth_score}/100
- Neighborhood demonstrates {"strong" if growth_score > 75 else "steady"} growth indicators
- Quality school district with ratings above regional average
- {"High" if growth_score > 80 else "Moderate"} demographic and economic stability

### INVESTMENT METRICS

**Rental Yield**: {analytics.get('rental_yield', 4.5):.2f}%
**Projected Appreciation**: {analytics.get('appreciation_rate', 3.8):.1f}% annually
**Demand Index**: {analytics.get('demand_index', 75)}/100

The property shows {"strong" if analytics.get('demand_index', 75) > 80 else "solid"} demand characteristics with below-average days on market, indicating {"high" if analytics.get('demand_index', 75) > 80 else "moderate"} liquidity.

### AMENITY & CONDITION ANALYSIS

**Amenity Score**: {analytics.get('amenity_score', 60):.1f}/100
**Structural Score**: {analytics.get('structural_score', 70):.1f}/100

The property features {"modern" if analytics.get('structural_score', 70) > 80 else "well-maintained"} construction and {"premium" if analytics.get('amenity_score', 60) > 75 else "standard"} amenities for its market segment.

### RISK ASSESSMENT

**Risk Score**: {risk_score}/100 (Lower is better)

Key considerations:
- Market liquidity: {"High" if risk_score < 40 else "Moderate"}
- Price volatility: {"Low" if risk_score < 40 else "Moderate"}
- Neighborhood stability: {"High" if risk_score < 40 else "Moderate"}

### INVESTMENT THESIS

**Recommendation**: {"STRONG BUY" if valuation_score > 85 and growth_score > 80 else "BUY" if valuation_score > 75 else "HOLD"}
**Confidence**: {"High" if valuation_score > 80 else "Moderate"}

This property represents a {"compelling" if valuation_score > 85 else "solid"} investment opportunity for {"value-oriented" if valuation_score > 75 else "balanced"} investors. The combination of {"strong" if growth_score > 75 else "stable"} neighborhood fundamentals, {"competitive" if 75 <= valuation_score <= 85 else "attractive"} pricing, and {"low" if risk_score < 40 else "manageable"} risk profile suggests {"excellent" if valuation_score > 85 else "good"} potential for both rental income and capital appreciation.

**Target Hold Period**: 5-7 years
**Expected IRR**: {analytics.get('appreciation_rate', 3.8) + analytics.get('rental_yield', 4.5):.1f}%
"""
        
        return {
            "property_id": property_data.get("id"),
            "summary": f"This property presents a {'strong' if valuation_score > 80 else 'moderate'} investment opportunity with a valuation score of {valuation_score}/100 and growth potential of {growth_score}/100.",
            "investment_thesis": f"{'STRONG BUY' if valuation_score > 85 and growth_score > 80 else 'BUY' if valuation_score > 75 else 'HOLD'} - This property represents a {'compelling' if valuation_score > 85 else 'solid'} investment with {'excellent' if valuation_score > 85 else 'good'} appreciation potential.",
            "full_report": report,
            "overall_score": round((valuation_score + growth_score + (100 - risk_score)) / 3, 1),
            "valuation_score": valuation_score,
            "growth_score": growth_score,
            "risk_score": risk_score,
            "sections": self._parse_audit_sections(report)
        }
