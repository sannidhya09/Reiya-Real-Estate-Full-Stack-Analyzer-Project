'use client';

import { Property, StreetStats } from '@/types';
import { formatCurrency, formatNumber } from '@/lib/utils';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface ComparisonChartProps {
  property: Property;
  streetStats: StreetStats;
  comparison: any;
}

export function ComparisonChart({ property, streetStats, comparison }: ComparisonChartProps) {
  const chartData = [
    {
      metric: 'Price/Sqft',
      'This Property': property.price_per_sqft || 0,
      'Street Average': streetStats.avg_price_per_sqft || 0,
    },
    {
      metric: 'Square Feet',
      'This Property': property.sqft || 0,
      'Street Average': streetStats.avg_sqft || 0,
    },
  ];

  return (
    <div>
      {/* Comparison Stats */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <ComparisonStat
          label="Price vs Street"
          value={comparison.ppsf_vs_street !== undefined ? `${comparison.ppsf_vs_street > 0 ? '+' : ''}${comparison.ppsf_vs_street.toFixed(1)}%` : 'N/A'}
          positive={comparison.ppsf_vs_street !== undefined && comparison.ppsf_vs_street < 0}
        />
        <ComparisonStat
          label="Price Percentile"
          value={comparison.price_percentile !== undefined ? `${comparison.price_percentile}th` : 'N/A'}
          positive={comparison.price_percentile !== undefined && comparison.price_percentile < 50}
        />
        <ComparisonStat
          label="Z-Score"
          value={comparison.price_zscore !== undefined ? comparison.price_zscore.toFixed(2) : 'N/A'}
          positive={comparison.price_zscore !== undefined && comparison.price_zscore < 0}
        />
      </div>

      {/* Chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200" />
            <XAxis dataKey="metric" className="text-xs" />
            <YAxis className="text-xs" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '0.5rem',
              }}
            />
            <Legend />
            <Bar dataKey="This Property" fill="#0ea5e9" />
            <Bar dataKey="Street Average" fill="#94a3b8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Street Stats Summary */}
      <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
        <div>
          <div className="text-gray-500">Street Properties</div>
          <div className="font-semibold text-gray-900">{streetStats.property_count || 'N/A'}</div>
        </div>
        <div>
          <div className="text-gray-500">Median Price</div>
          <div className="font-semibold text-gray-900">{formatCurrency(streetStats.median_price)}</div>
        </div>
        <div>
          <div className="text-gray-500">Average Price</div>
          <div className="font-semibold text-gray-900">{formatCurrency(streetStats.avg_price)}</div>
        </div>
        <div>
          <div className="text-gray-500">Avg Sqft</div>
          <div className="font-semibold text-gray-900">{formatNumber(streetStats.avg_sqft)}</div>
        </div>
      </div>
    </div>
  );
}

function ComparisonStat({
  label,
  value,
  positive,
}: {
  label: string;
  value: string;
  positive: boolean;
}) {
  return (
    <div className="text-center">
      <div className="text-sm text-gray-500 mb-1">{label}</div>
      <div className={`text-2xl font-bold ${positive ? 'text-green-600' : 'text-gray-900'}`}>
        {value}
      </div>
    </div>
  );
}
