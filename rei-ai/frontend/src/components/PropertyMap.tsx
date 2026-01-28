'use client';

import { useState, useMemo } from 'react';
import Map, { Marker, Popup, NavigationControl } from 'react-map-gl';
import { Property } from '@/types';
import { formatCurrency } from '@/lib/utils';
import { Home } from 'lucide-react';
import Link from 'next/link';

interface PropertyMapProps {
  properties: Property[];
}

const MAPBOX_TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || '';

export function PropertyMap({ properties }: PropertyMapProps) {
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(null);

  // Calculate center of all properties
  const center = useMemo(() => {
    if (properties.length === 0) {
      return { latitude: 33.0198, longitude: -96.6989 }; // Plano, TX default
    }

    const avgLat = properties.reduce((sum, p) => sum + p.latitude, 0) / properties.length;
    const avgLng = properties.reduce((sum, p) => sum + p.longitude, 0) / properties.length;

    return { latitude: avgLat, longitude: avgLng };
  }, [properties]);

  // If no Mapbox token, show fallback
  if (!MAPBOX_TOKEN) {
    return (
      <div className="card">
        <div className="text-center py-20">
          <Home className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Map View Unavailable</h3>
          <p className="text-gray-600 mb-4">
            Add your Mapbox access token to .env.local to enable the map view.
          </p>
          <p className="text-sm text-gray-500">
            Get a free token at{' '}
            <a
              href="https://www.mapbox.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-brand-600 hover:underline"
            >
              mapbox.com
            </a>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="card p-0 overflow-hidden" style={{ height: '600px' }}>
      <Map
        initialViewState={{
          latitude: center.latitude,
          longitude: center.longitude,
          zoom: 12,
        }}
        style={{ width: '100%', height: '100%' }}
        mapStyle="mapbox://styles/mapbox/streets-v12"
        mapboxAccessToken={MAPBOX_TOKEN}
      >
        <NavigationControl position="top-right" />

        {/* Property Markers */}
        {properties.map((property) => (
          <Marker
            key={property.id}
            latitude={property.latitude}
            longitude={property.longitude}
            onClick={(e) => {
              e.originalEvent.stopPropagation();
              setSelectedProperty(property);
            }}
          >
            <div className="cursor-pointer transform hover:scale-110 transition-transform">
              <div className="bg-brand-600 text-white px-2 py-1 rounded-full text-xs font-semibold shadow-lg">
                {formatCurrency(property.list_price)}
              </div>
            </div>
          </Marker>
        ))}

        {/* Popup for selected property */}
        {selectedProperty && (
          <Popup
            latitude={selectedProperty.latitude}
            longitude={selectedProperty.longitude}
            onClose={() => setSelectedProperty(null)}
            closeOnClick={false}
            offset={15}
          >
            <div className="p-2">
              <h3 className="font-semibold text-sm mb-2">{selectedProperty.address}</h3>
              <p className="text-lg font-bold text-brand-600 mb-2">
                {formatCurrency(selectedProperty.list_price)}
              </p>
              <div className="text-xs text-gray-600 space-y-1">
                <p>{selectedProperty.bedrooms} beds • {selectedProperty.bathrooms} baths</p>
                <p>{selectedProperty.sqft} sqft</p>
              </div>
              <Link
                href={`/property/${selectedProperty.id}`}
                className="block mt-3 text-xs text-brand-600 font-medium hover:underline"
              >
                View Details →
              </Link>
            </div>
          </Popup>
        )}
      </Map>
    </div>
  );
}
