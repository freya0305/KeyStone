'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { apiRequest } from '@/lib/api';

interface Application {
  id: string;
  employer: string;
  role: string;
  status: string;
  applied_at: string;
  job_url?: string;
  has_response?: boolean;
}

type BatchUpdateStatus = 'got_response' | 'no_news' | 'skip';

interface BatchUpdate {
  id: string;
  status: BatchUpdateStatus;
}

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [timeFilter, setTimeFilter] = useState('30');
  const [batchMode, setBatchMode] = useState(false);
  const [batchUpdates, setBatchUpdates] = useState<Record<string, BatchUpdate>>({});
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    apiRequest<Application[]>('/job-seeker/applications')
      .then(setApplications)
      .catch(() => setApplications([]))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    const pending = applications.filter(
      (app) => app.status === 'applied' || app.status === 'screening'
    ).length;
    setPendingCount(pending);
  }, [applications]);

  const handleBatchUpdate = (appId: string, status: BatchUpdateStatus) => {
    setBatchUpdates((prev) => ({ ...prev, [appId]: { id: appId, status } }));
  };

  const submitBatchUpdate = async () => {
    const updates = Object.values(batchUpdates).filter(Boolean) as BatchUpdate[];
    if (updates.length === 0) return;

    try {
      await apiRequest('/job-seeker/applications/batch-update', {
        method: 'POST',
        body: { updates },
      });
      setBatchMode(false);
      setBatchUpdates({});
      window.location.reload();
    } catch (err) {
      console.error('Batch update failed:', err);
    }
  };

  const filtered = applications.filter((app) => {
    if (filter === 'all') return true;
    return app.status.toLowerCase() === filter.toLowerCase();
  });

  const statusColors: Record<string, string> = {
    applied: 'bg-blue-100 text-blue-700',
    screening: 'bg-yellow-100 text-yellow-700',
    interview: 'bg-purple-100 text-purple-700',
    offer: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700',
    withdrawn: 'bg-gray-100 text-gray-700',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Applications</h1>
          <p className="text-gray-600">Track your job applications</p>
        </div>
        <Link
          href="/app/new"
          className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
        >
          + New Application
        </Link>
      </div>

      {/* Batch Update Banner */}
      {!loading && pendingCount > 0 && !batchMode && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">📬</span>
            <div>
              <p className="font-medium text-blue-900">
                You have {pendingCount} pending applications
              </p>
              <p className="text-sm text-blue-700">Update them in batch to get better insights.</p>
            </div>
          </div>
          <button
            onClick={() => setBatchMode(true)}
            className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
          >
            Update Now
          </button>
        </div>
      )}

      {/* Batch Update Mode Banner */}
      {batchMode && (
        <div className="bg-brand-50 border border-brand-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <span className="font-medium text-brand-900">Batch Update Mode</span>
              <span className="text-sm text-brand-700">
                ({Object.keys(batchUpdates).length} updated)
              </span>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => {
                  setBatchMode(false);
                  setBatchUpdates({});
                }}
                className="px-3 py-1.5 text-sm border rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={submitBatchUpdate}
                disabled={Object.keys(batchUpdates).length === 0}
                className="px-3 py-1.5 text-sm bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50"
              >
                Submit Updates
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-4">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-3 py-2 border rounded-lg text-sm"
        >
          <option value="all">All statuses</option>
          <option value="applied">Applied</option>
          <option value="screening">Screening</option>
          <option value="interview">Interview</option>
          <option value="offer">Offer</option>
          <option value="rejected">Rejected</option>
        </select>
        <select
          value={timeFilter}
          onChange={(e) => setTimeFilter(e.target.value)}
          className="px-3 py-2 border rounded-lg text-sm"
        >
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
          <option value="all">All time</option>
        </select>
      </div>

      {/* Loading */}
      {loading && <div className="text-center py-12 text-gray-500">Loading...</div>}

      {/* Empty State */}
      {!loading && filtered.length === 0 && (
        <div className="bg-white border rounded-xl p-12 text-center">
          <div className="text-4xl mb-4">📋</div>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">No applications yet</h2>
          <p className="text-gray-600 mb-6">
            Start tracking your job applications to see your progress.
          </p>
          <Link
            href="/app/new"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Add your first application
          </Link>
        </div>
      )}

      {/* Applications List */}
      {!loading && filtered.length > 0 && (
        <div className="bg-white border rounded-xl divide-y">
          {filtered.map((app) => (
            <div key={app.id} className="p-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <Link href={`/app/applications/${app.id}`} className="flex-1 min-w-0">
                  <div className="flex items-center gap-3">
                    <span className="font-medium text-gray-900 truncate">{app.employer}</span>
                    <span
                      className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColors[app.status.toLowerCase()] || 'bg-gray-100 text-gray-600'}`}
                    >
                      {app.status}
                    </span>
                  </div>
                  <div className="text-sm text-gray-500 truncate mt-0.5">{app.role}</div>
                </Link>
                <div className="text-sm text-gray-400 ml-4">
                  {new Date(app.applied_at).toLocaleDateString('en-SG', {
                    day: 'numeric',
                    month: 'short',
                  })}
                </div>
              </div>

              {/* Batch Update Buttons */}
              {batchMode && (app.status === 'applied' || app.status === 'screening') && (
                <div className="flex gap-2 mt-3 pt-3 border-t">
                  <button
                    onClick={() => handleBatchUpdate(app.id, 'got_response')}
                    className={`flex-1 py-1.5 text-xs rounded-lg transition-colors ${
                      batchUpdates[app.id]?.status === 'got_response'
                        ? 'bg-green-500 text-white'
                        : 'bg-green-50 text-green-700 hover:bg-green-100 border border-green-200'
                    }`}
                  >
                    Got response
                  </button>
                  <button
                    onClick={() => handleBatchUpdate(app.id, 'no_news')}
                    className={`flex-1 py-1.5 text-xs rounded-lg transition-colors ${
                      batchUpdates[app.id]?.status === 'no_news'
                        ? 'bg-yellow-500 text-white'
                        : 'bg-yellow-50 text-yellow-700 hover:bg-yellow-100 border border-yellow-200'
                    }`}
                  >
                    No news
                  </button>
                  <button
                    onClick={() => handleBatchUpdate(app.id, 'skip')}
                    className={`flex-1 py-1.5 text-xs rounded-lg transition-colors ${
                      batchUpdates[app.id]?.status === 'skip'
                        ? 'bg-gray-500 text-white'
                        : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200'
                    }`}
                  >
                    Skip
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
