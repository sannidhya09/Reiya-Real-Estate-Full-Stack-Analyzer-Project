'use client';

import { use, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { api } from '@/lib/api';
import {
  formatCurrency,
  formatNumber,
  formatPercent,
  getScoreColor,
  getScoreBgColor,
  getInvestmentRecommendation,
  yearsAgo,
} from '@/lib/utils';
import {
  Home,
  ArrowLeft,
  Bed,
  Bath,
  Square,
  Calendar,
  TrendingUp,
  AlertCircle,
  FileText,
  BarChart3,
  MapPin,
} from 'lucide-react';
import { ScoreGauge } from '@/components/ScoreGauge';
import { ComparisonChart } from '@/components/ComparisonChart';
import { AIAuditReport } from '@/components/AIAuditReport';
import toast from 'react-hot-toast';

interface PageProps {
  params: Promise<{ id: string }>;
}

export default function PropertyDetailPage({ params }: PageProps) {
  const resolvedParams = use(params);
  const propertyId = parseInt(resolvedParams.id);
  const [showAudit, setShowAudit] = useState(false);

  // Fetch property analysis
  const { data: analysis, isLoading } = useQuery({
    queryKey: ['propertyAnalysis', propertyId],
    queryFn: () => api.getPropertyAnalysis(propertyId),
  });

  // Generate AI audit
  const { data: audit, isLoading: auditLoading, refetch: generateAudit } = useQuery({
    queryKey: ['audit', propertyId],
    queryFn: () => api.generateAudit(propertyId),
    enabled: false, // Only run when explicitly called
  });

  const handleGenerateAudit = async () => {
    const toastId = toast.loading('Generating AI audit...');
    try {
      await generateAudit();
      setShowAudit(true);
      toast.success('AI audit generated!', { id: toastId });
    } catch (error) {
      toast.error('Failed to generate audit', { id: toastId });
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">Property not found</p>
          <Link href="/" className="text-brand-600 hover:underline">
            ← Back to Home
          </Link>
        </div>
      </div>
    );
  }

  const { property, scores, ai_scores, street_stats, street_comparison, neighborhood } = analysis;
  const recommendation = getInvestmentRecommendation(
    ai_scores.ai_valuation_score,
    ai_scores.ai_growth_score,
    ai_scores.ai_risk_score
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Link href="/" className="inline-flex items-center gap-2 text-brand-600 hover:text-brand-700 mb-4">
            <ArrowLeft className="w-4 h-4" />
            Back to Properties
          </Link>
          
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{property.address}</h1>
              <p className="text-gray-600 mt-1 flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                {property.city}, {property.state} {property.zip_code}
              </p>
            </div>
            <div className={`${recommendation.color} text-white px-6 py-3 rounded-lg font-bold text-lg`}>
              {recommendation.label}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Property Details */}
          <div className="lg:col-span-2 space-y-6">
            {/* Price & Basic Info */}
            <div className="card">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <div className="text-4xl font-bold text-gray-900 mb-2">
                    {formatCurrency(property.list_price)}
                  </div>
                  <div className="text-xl text-gray-600">
                    {formatCurrency(property.price_per_sqft)}/sqft
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-500">Status</div>
                  <div className={`text-lg font-semibold ${property.status === 'Active' ? 'text-green-600' : 'text-yellow-600'}`}>
                    {property.status}
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <DetailItem icon={<Bed />} label="Bedrooms" value={property.bedrooms?.toString() || 'N/A'} />
                <DetailItem icon={<Bath />} label="Bathrooms" value={property.bathrooms?.toString() || 'N/A'} />
                <DetailItem icon={<Square />} label="Square Feet" value={formatNumber(property.sqft)} />
                <DetailItem icon={<Calendar />} label="Year Built" value={property.year_built?.toString() || 'N/A'} />
              </div>

              {property.year_built && (
                <div className="mt-4 text-sm text-gray-600">
                  Property Age: {yearsAgo(property.year_built)} years old
                </div>
              )}
            </div>

            {/* AI Scores */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                AI Investment Scores
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <ScoreGauge
                  label="Valuation Score"
                  score={ai_scores.ai_valuation_score}
                  description="Price competitiveness"
                />
                <ScoreGauge
                  label="Growth Score"
                  score={ai_scores.ai_growth_score}
                  description="Appreciation potential"
                />
                <ScoreGauge
                  label="Risk Score"
                  score={ai_scores.ai_risk_score}
                  description="Investment risk (lower is better)"
                  inverted
                />
              </div>
            </div>

            {/* Street Comparison */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Street Comparison</h2>
              <ComparisonChart
                property={property}
                streetStats={street_stats}
                comparison={street_comparison}
              />
            </div>

            {/* Investment Metrics */}
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Investment Metrics</h2>
              
              <div className="grid grid-cols-2 gap-4">
                <MetricCard
                  label="Rental Yield"
                  value={formatPercent(scores.rental_yield)}
                  description="Estimated annual return"
                />
                <MetricCard
                  label="Appreciation Rate"
                  value={formatPercent(scores.appreciation_rate)}
                  description="Expected yearly growth"
                />
                <MetricCard
                  label="Demand Index"
                  value={`${scores.demand_index}/100`}
                  description="Market demand strength"
                />
                <MetricCard
                  label="Days on Market"
                  value={property.days_on_market?.toString() || 'N/A'}
                  description="Time listed for sale"
                />
              </div>
            </div>

            {/* AI Audit Button & Display */}
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  AI Investment Audit
                </h2>
                {!showAudit && (
                  <button
                    onClick={handleGenerateAudit}
                    disabled={auditLoading}
                    className="btn-primary disabled:opacity-50"
                  >
                    {auditLoading ? 'Generating...' : 'Generate Full Audit'}
                  </button>
                )}
              </div>

              {showAudit && audit && <AIAuditReport audit={audit} />}
            </div>
          </div>

          {/* Right Column - Additional Info */}
          <div className="space-y-6">
            {/* Property Quality Scores */}
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-4">Property Quality</h3>
              <div className="space-y-3">
                <ScoreBar label="Amenity Score" score={scores.amenity_score} />
                <ScoreBar label="Structural Score" score={scores.structural_score} />
                <ScoreBar label="Location Score" score={scores.location_score} />
              </div>
            </div>

            {/* Neighborhood Stats */}
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-4">Neighborhood Data</h3>
              <div className="space-y-3 text-sm">
                <StatRow label="Median Income" value={formatCurrency(neighborhood.median_income)} />
                <StatRow label="Population Growth" value={formatPercent(neighborhood.population_growth)} />
                <StatRow label="School Quality" value={`${neighborhood.school_quality_avg.toFixed(1)}/10`} />
                <StatRow label="Crime Rate" value={`${neighborhood.crime_rate.toFixed(1)} per 1000`} />
              </div>
            </div>

            {/* Quick Facts */}
            <div className="card bg-gradient-to-br from-brand-50 to-brand-100 border-brand-200">
              <h3 className="font-semibold text-brand-900 mb-4 flex items-center gap-2">
                <AlertCircle className="w-5 h-5" />
                Quick Insights
              </h3>
              <ul className="space-y-2 text-sm text-brand-900">
                {street_comparison.ppsf_vs_street !== undefined && (
                  <li>
                    • {street_comparison.ppsf_vs_street > 0 ? 'Premium' : 'Discount'} of{' '}
                    {Math.abs(street_comparison.ppsf_vs_street).toFixed(1)}% vs street average
                  </li>
                )}
                {property.days_on_market && property.days_on_market < 30 && (
                  <li>• High demand: Only {property.days_on_market} days on market</li>
                )}
                {ai_scores.ai_valuation_score > 80 && (
                  <li>• Excellent valuation opportunity</li>
                )}
                {ai_scores.ai_growth_score > 75 && (
                  <li>• Strong growth potential in this area</li>
                )}
                {ai_scores.ai_risk_score < 40 && (
                  <li>• Low-risk investment profile</li>
                )}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Helper Components
function DetailItem({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex items-center gap-2">
      <div className="text-gray-400">{icon}</div>
      <div>
        <div className="text-xs text-gray-500">{label}</div>
        <div className="font-semibold text-gray-900">{value}</div>
      </div>
    </div>
  );
}

function MetricCard({ label, value, description }: { label: string; value: string; description: string }) {
  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <div className="text-2xl font-bold text-gray-900 mb-1">{value}</div>
      <div className="text-sm font-medium text-gray-900">{label}</div>
      <div className="text-xs text-gray-500 mt-1">{description}</div>
    </div>
  );
}

function ScoreBar({ label, score }: { label: string; score: number }) {
  return (
    <div>
      <div className="flex items-center justify-between text-sm mb-1">
        <span className="text-gray-700">{label}</span>
        <span className={`font-semibold ${getScoreColor(score)}`}>{score.toFixed(1)}/100</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${score >= 80 ? 'bg-green-500' : score >= 60 ? 'bg-yellow-500' : 'bg-red-500'}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}

function StatRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-gray-600">{label}</span>
      <span className="font-semibold text-gray-900">{value}</span>
    </div>
  );
}
