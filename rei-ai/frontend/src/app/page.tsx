'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { PropertyCard } from '@/components/PropertyCard';
import { PropertyMap } from '@/components/PropertyMap';
import { CityStatsCard } from '@/components/CityStatsCard';
import { PropertyFilters as IPropertyFilters } from '@/types';
import { Search, MapPin, TrendingUp, Home } from 'lucide-react';
import toast from 'react-hot-toast';

export default function HomePage() {
  const [selectedCity, setSelectedCity] = useState('Plano');
  const [viewMode, setViewMode] = useState<'grid' | 'map'>('grid');
  const [filters, setFilters] = useState<IPropertyFilters>({
    city: 'Plano',
  });

  // Fetch properties
  const { data: properties = [], isLoading, error } = useQuery({
    queryKey: ['properties', filters],
    queryFn: () => api.getProperties(filters),
  });

  // Fetch city stats
  const { data: cityStats } = useQuery({
    queryKey: ['cityStats', selectedCity],
    queryFn: () => api.getCityStats(selectedCity),
    enabled: !!selectedCity,
  });

  const handleCityChange = (city: string) => {
    setSelectedCity(city);
    setFilters({ ...filters, city });
  };

  const handleSync = async () => {
    const toastId = toast.loading('Syncing properties...');
    try {
      await api.syncProperties(selectedCity);
      toast.success('Properties synced successfully!', { id: toastId });
      window.location.reload();
    } catch (error) {
      toast.error('Failed to sync properties', { id: toastId });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                <Home className="w-8 h-8 text-brand-600" />
                REI-AI
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Real Estate Intelligence & Analytics Platform
              </p>
            </div>
            <button
              onClick={handleSync}
              className="btn-primary flex items-center gap-2"
            >
              <TrendingUp className="w-4 h-4" />
              Sync Data
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* City Selector & View Toggle */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="flex-1">
            <label className="label">Select City</label>
            <select
              value={selectedCity}
              onChange={(e) => handleCityChange(e.target.value)}
              className="input"
            >
              <option value="Plano">Plano, TX</option>
              <option value="Frisco">Frisco, TX</option>
              <option value="Richardson">Richardson, TX</option>
            </select>
          </div>

          <div className="flex-1">
            <label className="label">Price Range</label>
            <select
              onChange={(e) => {
                const value = e.target.value;
                if (value === 'all') {
                  setFilters({ ...filters, min_price: undefined, max_price: undefined });
                } else {
                  const [min, max] = value.split('-').map(Number);
                  setFilters({ ...filters, min_price: min, max_price: max });
                }
              }}
              className="input"
            >
              <option value="all">All Prices</option>
              <option value="0-300000">Under $300K</option>
              <option value="300000-500000">$300K - $500K</option>
              <option value="500000-750000">$500K - $750K</option>
              <option value="750000-1000000">$750K - $1M</option>
              <option value="1000000-10000000">Over $1M</option>
            </select>
          </div>

          <div className="flex items-end gap-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                viewMode === 'grid'
                  ? 'bg-brand-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Grid
            </button>
            <button
              onClick={() => setViewMode('map')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                viewMode === 'map'
                  ? 'bg-brand-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Map
            </button>
          </div>
        </div>

        {/* City Stats */}
        {cityStats && <CityStatsCard stats={cityStats} />}

        {/* Properties Display */}
        {isLoading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
          </div>
        ) : error ? (
          <div className="text-center py-20">
            <p className="text-red-600">Error loading properties. Please try again.</p>
          </div>
        ) : viewMode === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {properties.length === 0 ? (
              <div className="col-span-full text-center py-20">
                <MapPin className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No properties found. Try adjusting your filters.</p>
              </div>
            ) : (
              properties.map((property) => (
                <PropertyCard key={property.id} property={property} />
              ))
            )}
          </div>
        ) : (
          <PropertyMap properties={properties} />
        )}
      </main>
    </div>
  );
}