'use client';

import { CityStats } from '@/types';
import { formatCurrency, formatNumber } from '@/lib/utils';
import { Home, DollarSign, TrendingUp, Activity } from 'lucide-react';

interface CityStatsCardProps {
  stats: CityStats;
}

export function CityStatsCard({ stats }: CityStatsCardProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <StatItem
        icon={<Home className="w-5 h-5" />}
        label="Total Properties"
        value={formatNumber(stats.total_properties)}
        bgColor="bg-blue-50"
        iconColor="text-blue-600"
      />
      <StatItem
        icon={<DollarSign className="w-5 h-5" />}
        label="Median Price"
        value={formatCurrency(stats.median_price)}
        bgColor="bg-green-50"
        iconColor="text-green-600"
      />
      <StatItem
        icon={<TrendingUp className="w-5 h-5" />}
        label="Avg Price/Sqft"
        value={formatCurrency(stats.avg_price_per_sqft)}
        bgColor="bg-purple-50"
        iconColor="text-purple-600"
      />
      <StatItem
        icon={<Activity className="w-5 h-5" />}
        label="Active Listings"
        value={formatNumber(stats.active_listings)}
        bgColor="bg-orange-50"
        iconColor="text-orange-600"
      />
    </div>
  );
}

interface StatItemProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  bgColor: string;
  iconColor: string;
}

function StatItem({ icon, label, value, bgColor, iconColor }: StatItemProps) {
  return (
    <div className="stat-card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{label}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`${bgColor} ${iconColor} p-3 rounded-lg`}>
          {icon}
        </div>
      </div>
    </div>
  );
}
