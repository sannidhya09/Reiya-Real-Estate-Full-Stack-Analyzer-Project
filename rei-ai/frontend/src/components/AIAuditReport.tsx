'use client';

import { AIAudit } from '@/types';
import { formatPercent, getScoreColor } from '@/lib/utils';
import { TrendingUp, AlertTriangle, CheckCircle, FileDown } from 'lucide-react';

interface AIAuditReportProps {
  audit: AIAudit;
}

export function AIAuditReport({ audit }: AIAuditReportProps) {
  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([audit.full_report], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `property-audit-${audit.property_id}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="space-y-6">
      {/* Summary Card */}
      <div className="bg-gradient-to-br from-brand-50 to-brand-100 rounded-lg p-6 border border-brand-200">
        <div className="flex items-start justify-between mb-4">
          <h3 className="text-lg font-bold text-brand-900">Executive Summary</h3>
          <button
            onClick={handleDownload}
            className="flex items-center gap-2 text-sm text-brand-700 hover:text-brand-900"
          >
            <FileDown className="w-4 h-4" />
            Download Report
          </button>
        </div>
        <p className="text-brand-900 leading-relaxed">{audit.summary}</p>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <ScoreCard
          label="Overall Score"
          score={audit.overall_score}
          icon={<CheckCircle className="w-5 h-5" />}
        />
        <ScoreCard
          label="Valuation"
          score={audit.valuation_score}
          icon={<TrendingUp className="w-5 h-5" />}
        />
        <ScoreCard
          label="Growth Potential"
          score={audit.growth_score}
          icon={<TrendingUp className="w-5 h-5" />}
        />
      </div>

      {/* Investment Thesis */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-green-600" />
          Investment Thesis
        </h3>
        <p className="text-gray-700 leading-relaxed">{audit.investment_thesis}</p>
      </div>

      {/* Full Report */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Detailed Analysis</h3>
        <div className="prose prose-sm max-w-none">
          <pre className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed font-sans">
            {audit.full_report}
          </pre>
        </div>
      </div>

      {/* Risk Factors */}
      {audit.risk_score > 50 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-yellow-900 mb-3 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            Risk Considerations
          </h3>
          <p className="text-yellow-800">
            This property has a risk score of {audit.risk_score.toFixed(1)}/100. 
            Consider the following factors before making an investment decision:
          </p>
          <ul className="mt-3 space-y-2 text-sm text-yellow-800">
            <li>• Review market conditions and economic indicators</li>
            <li>• Conduct thorough property inspection</li>
            <li>• Verify all financial projections</li>
            <li>• Consult with real estate professionals</li>
          </ul>
        </div>
      )}
    </div>
  );
}

function ScoreCard({
  label,
  score,
  icon,
}: {
  label: string;
  score: number;
  icon: React.ReactNode;
}) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-600">{label}</span>
        <span className="text-gray-400">{icon}</span>
      </div>
      <div className={`text-3xl font-bold ${getScoreColor(score)}`}>
        {score.toFixed(1)}
      </div>
      <div className="text-xs text-gray-500 mt-1">/ 100</div>
    </div>
  );
}
