/**
 * Utility Functions
 */

/**
 * Format currency
 */
export function formatCurrency(value: number | undefined): string {
  if (value === undefined || value === null) return 'N/A';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  }).format(value);
}

/**
 * Format number with commas
 */
export function formatNumber(value: number | undefined): string {
  if (value === undefined || value === null) return 'N/A';
  return new Intl.NumberFormat('en-US').format(value);
}

/**
 * Format percentage
 */
export function formatPercent(value: number | undefined, decimals: number = 1): string {
  if (value === undefined || value === null) return 'N/A';
  return `${value.toFixed(decimals)}%`;
}

/**
 * Get score color based on value
 */
export function getScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  return 'text-red-600';
}

/**
 * Get score background color
 */
export function getScoreBgColor(score: number): string {
  if (score >= 80) return 'bg-green-100';
  if (score >= 60) return 'bg-yellow-100';
  return 'bg-red-100';
}

/**
 * Get risk level
 */
export function getRiskLevel(score: number): string {
  if (score < 30) return 'Low';
  if (score < 60) return 'Moderate';
  return 'High';
}

/**
 * Get investment recommendation
 */
export function getInvestmentRecommendation(
  valuationScore: number,
  growthScore: number,
  riskScore: number
): { label: string; color: string } {
  const avgScore = (valuationScore + growthScore + (100 - riskScore)) / 3;
  
  if (avgScore >= 80) {
    return { label: 'STRONG BUY', color: 'bg-green-600' };
  } else if (avgScore >= 70) {
    return { label: 'BUY', color: 'bg-green-500' };
  } else if (avgScore >= 55) {
    return { label: 'HOLD', color: 'bg-yellow-500' };
  } else {
    return { label: 'CONSIDER', color: 'bg-gray-500' };
  }
}

/**
 * Truncate text
 */
export function truncate(str: string, length: number): string {
  if (str.length <= length) return str;
  return str.slice(0, length) + '...';
}

/**
 * Delay function for demo purposes
 */
export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Format address
 */
export function formatAddress(property: {
  address?: string;
  city?: string;
  state?: string;
  zip_code?: string;
}): string {
  const parts = [];
  if (property.address) parts.push(property.address);
  if (property.city) parts.push(property.city);
  if (property.state) parts.push(property.state);
  if (property.zip_code) parts.push(property.zip_code);
  return parts.join(', ');
}

/**
 * Calculate years ago
 */
export function yearsAgo(year: number): number {
  return new Date().getFullYear() - year;
}

/**
 * Class name utility (simple version of clsx)
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}
