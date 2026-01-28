/**
 * API Client for REI-AI Backend
 */
import axios from 'axios';
import type { Property, PropertyAnalysis, AIAudit, CityStats, PropertyFilters } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Properties
  async getProperties(filters?: PropertyFilters): Promise<Property[]> {
    const { data } = await apiClient.get('/properties/', { params: filters });
    return data;
  },

  async getProperty(id: number): Promise<Property> {
    const { data } = await apiClient.get(`/properties/${id}`);
    return data;
  },

  async getPropertyAnalysis(id: number): Promise<PropertyAnalysis> {
    const { data } = await apiClient.get(`/properties/${id}/analysis`);
    return data;
  },

  async generateAudit(id: number): Promise<AIAudit> {
    const { data } = await apiClient.post(`/properties/${id}/audit`);
    return data;
  },

  async getNearbyProperties(
    latitude: number,
    longitude: number,
    radiusMiles: number = 0.5
  ): Promise<Property[]> {
    const { data } = await apiClient.get('/properties/nearby/search', {
      params: { latitude, longitude, radius_miles: radiusMiles },
    });
    return data;
  },

  async getCityStats(city: string): Promise<CityStats> {
    const { data } = await apiClient.get(`/properties/city/${city}/stats`);
    return data;
  },

  async syncProperties(city: string, state: string = 'TX'): Promise<{ count: number }> {
    const { data } = await apiClient.post(`/properties/sync/${city}`, null, {
      params: { state },
    });
    return data;
  },

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const { data } = await apiClient.get('/health');
    return data;
  },
};

export default api;
