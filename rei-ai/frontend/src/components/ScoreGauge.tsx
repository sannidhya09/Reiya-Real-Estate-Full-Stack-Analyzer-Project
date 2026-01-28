'use client';

import { getScoreColor, getScoreBgColor } from '@/lib/utils';

interface ScoreGaugeProps {
  label: string;
  score: number;
  description: string;
  inverted?: boolean;
}

export function ScoreGauge({ label, score, description, inverted = false }: ScoreGaugeProps) {
  // For inverted scores (like risk), flip the color logic
  const displayScore = inverted ? 100 - score : score;
  
  return (
    <div className="text-center">
      <div className="relative inline-flex items-center justify-center mb-3">
        {/* Background circle */}
        <svg className="w-32 h-32 transform -rotate-90">
          <circle
            cx="64"
            cy="64"
            r="56"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
            className="text-gray-200"
          />
          {/* Progress circle */}
          <circle
            cx="64"
            cy="64"
            r="56"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
            strokeDasharray={`${(displayScore / 100) * 351.86} 351.86`}
            className={
              displayScore >= 80
                ? 'text-green-500'
                : displayScore >= 60
                ? 'text-yellow-500'
                : 'text-red-500'
            }
            strokeLinecap="round"
          />
        </svg>
        
        {/* Score text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className={`text-3xl font-bold ${getScoreColor(displayScore)}`}>
              {score.toFixed(1)}
            </div>
            <div className="text-xs text-gray-500">/ 100</div>
          </div>
        </div>
      </div>
      
      <div className="font-semibold text-gray-900 mb-1">{label}</div>
      <div className="text-xs text-gray-600">{description}</div>
    </div>
  );
}
