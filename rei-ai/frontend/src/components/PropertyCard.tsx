'use client';

import Link from 'next/link';
import { Property } from '@/types';
import { formatCurrency, formatNumber, getScoreColor } from '@/lib/utils';
import { Bed, Bath, Home, TrendingUp, MapPin } from 'lucide-react';

interface PropertyCardProps {
  property: Property;
}

export function PropertyCard({ property }: PropertyCardProps) {
  const {
    id,
    address,
    list_price,
    bedrooms,
    bathrooms,
    sqft,
    price_per_sqft,
    ai_valuation_score,
    ai_growth_score,
  } = property;

  return (
    <Link href={`/property/${id}`}>
      <div className="card hover:shadow-xl transition-all duration-300 cursor-pointer group h-full">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="font-semibold text-lg text-gray-900 group-hover:text-brand-600 transition-colors line-clamp-2">
              {address}
            </h3>
            <p className="text-sm text-gray-500 mt-1 flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              {property.city}, {property.state}
            </p>
          </div>
        </div>

        {/* Price */}
        <div className="mb-4">
          <div className="text-2xl font-bold text-gray-900">
            {formatCurrency(list_price)}
          </div>
          <div className="text-sm text-gray-600">
            {formatCurrency(price_per_sqft)}/sqft
          </div>
        </div>

        {/* Property Details */}
        <div className="flex items-center gap-4 text-sm text-gray-700 mb-4">
          <div className="flex items-center gap-1">
            <Bed className="w-4 h-4 text-gray-400" />
            <span>{bedrooms || 'N/A'} beds</span>
          </div>
          <div className="flex items-center gap-1">
            <Bath className="w-4 h-4 text-gray-400" />
            <span>{bathrooms || 'N/A'} baths</span>
          </div>
          <div className="flex items-center gap-1">
            <Home className="w-4 h-4 text-gray-400" />
            <span>{formatNumber(sqft)} sqft</span>
          </div>
        </div>

        {/* AI Scores */}
        <div className="border-t border-gray-200 pt-4 space-y-2">
          {ai_valuation_score !== undefined && (
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Valuation Score</span>
              <span className={`font-semibold ${getScoreColor(ai_valuation_score)}`}>
                {ai_valuation_score.toFixed(1)}/100
              </span>
            </div>
          )}
          {ai_growth_score !== undefined && (
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />
                Growth Score
              </span>
              <span className={`font-semibold ${getScoreColor(ai_growth_score)}`}>
                {ai_growth_score.toFixed(1)}/100
              </span>
            </div>
          )}
        </div>

        {/* View Details Button */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="text-sm font-medium text-brand-600 group-hover:text-brand-700 flex items-center justify-between">
            View Full Analysis
            <span className="text-xl group-hover:translate-x-1 transition-transform">→</span>
          </div>
        </div>
      </div>
    </Link>
  );
}
