'use client';

import { useState, useEffect } from 'react';
import { apiRequest } from '@/lib/api';

interface DashboardData {
  total_applications: number;
  response_rate: number;
  stage_funnel: {
    applied: number;
    screening: number;
    interview: number;
    offer: number;
    rejected: number;
  };
  trend_data: Array<{ month: string; applications: number; responses: number }>;
}

interface Application {
  id: string;
  employer: string;
  role: string;
  status: string;
  applied_at: string;
  has_response: boolean;
}

const MIN_APPLICATIONS = 5;

export default function AnalyticsPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiRequest<DashboardData>('/analytics/dashboard').catch(() => null),
      apiRequest<Application[]>('/job-seeker/applications').catch(() => []),
    ]).then(([dashboardData, apps]) => {
      setData(dashboardData);
      setApplications(apps);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="mt-4 text-gray-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  const activeCount = applications.filter((a) => a.status !== 'withdrawn').length;

  if (activeCount < MIN_APPLICATIONS) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-3xl mx-auto px-4 py-16">
          <div className="bg-white border rounded-xl p-12 text-center">
            <div className="text-6xl mb-4">📊</div>
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Analytics Dashboard</h1>
            <p className="text-gray-600 mb-6">
              You need at least {MIN_APPLICATIONS} active applications before analytics are
              available.
            </p>
            <div className="bg-gray-50 rounded-lg p-4 mb-6 max-w-xs mx-auto">
              <div className="text-sm text-gray-500 mb-2">Your progress</div>
              <div className="flex items-center gap-2">
                <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-600 rounded-full transition-all"
                    style={{ width: `${Math.min(100, (activeCount / MIN_APPLICATIONS) * 100)}%` }}
                  />
                </div>
                <span className="text-sm font-medium text-gray-700">
                  {activeCount}/{MIN_APPLICATIONS}
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-500">
              Keep tracking your applications to unlock insights.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const funnelSteps = [
    { key: 'applied', label: 'Applied', color: 'bg-blue-500' },
    { key: 'screening', label: 'Screening', color: 'bg-yellow-500' },
    { key: 'interview', label: 'Interview', color: 'bg-purple-500' },
    { key: 'offer', label: 'Offer', color: 'bg-green-500' },
    { key: 'rejected', label: 'Rejected', color: 'bg-red-500' },
  ];

  const maxFunnel = Math.max(...Object.values(data?.stage_funnel || {}), 1);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600">Track your job search performance</p>
        </div>

        {/* Summary Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white border rounded-xl p-6">
            <div className="text-sm text-gray-500 mb-1">Total Applications</div>
            <div className="text-3xl font-bold text-gray-900">{applications.length}</div>
          </div>
          <div className="bg-white border rounded-xl p-6">
            <div className="text-sm text-gray-500 mb-1">Response Rate</div>
            <div className="text-3xl font-bold text-gray-900">
              {data?.response_rate ? `${Math.round(data.response_rate)}%` : '—'}
            </div>
          </div>
          <div className="bg-white border rounded-xl p-6">
            <div className="text-sm text-gray-500 mb-1">Active Applications</div>
            <div className="text-3xl font-bold text-gray-900">{activeCount}</div>
          </div>
        </div>

        {/* Stage Funnel */}
        <div className="bg-white border rounded-xl p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Application Funnel</h2>
          <div className="space-y-4">
            {funnelSteps.map((step) => {
              const count = data?.stage_funnel?.[step.key as keyof typeof data.stage_funnel] || 0;
              const percentage = (count / maxFunnel) * 100;
              return (
                <div key={step.key} className="flex items-center gap-4">
                  <div className="w-20 text-sm text-gray-600">{step.label}</div>
                  <div className="flex-1">
                    <div className="h-8 bg-gray-100 rounded-lg overflow-hidden">
                      <div
                        className={`h-full ${step.color} rounded-lg transition-all flex items-center justify-end pr-3`}
                        style={{ width: `${percentage}%` }}
                      >
                        <span className="text-white text-sm font-medium">{count}</span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Trend Chart */}
        <div className="bg-white border rounded-xl p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Monthly Trend</h2>
          {data?.trend_data && data.trend_data.length > 0 ? (
            <div className="overflow-x-auto">
              <div className="min-w-[400px]">
                <div className="flex items-end gap-4 h-48">
                  {data.trend_data.map((month, i) => {
                    const maxApps = Math.max(...data.trend_data.map((d) => d.applications), 1);
                    const height = (month.applications / maxApps) * 100;
                    return (
                      <div key={i} className="flex-1 flex flex-col items-center gap-2">
                        <div className="w-full flex flex-col items-center gap-1">
                          <div
                            className="w-full bg-blue-500 rounded-t"
                            style={{
                              height: `${height}%`,
                              minHeight: month.applications > 0 ? '4px' : '0',
                            }}
                          />
                          {month.responses > 0 && (
                            <div
                              className="w-1/2 bg-green-400 rounded-t"
                              style={{
                                height: `${(month.responses / maxApps) * 100}%`,
                                minHeight: '4px',
                              }}
                            />
                          )}
                        </div>
                        <div className="text-xs text-gray-500">{month.month}</div>
                      </div>
                    );
                  })}
                </div>
                <div className="flex gap-4 mt-4 justify-center">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-blue-500 rounded" />
                    <span className="text-sm text-gray-600">Applications</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-green-400 rounded" />
                    <span className="text-sm text-gray-600">Responses</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              Not enough data for trends yet. Check back after more applications.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
