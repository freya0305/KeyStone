"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { apiRequest } from '@/lib/api'

interface Application {
  id: string
  employer: string
  role: string
  status: string
  applied_at: string
  job_url?: string
}

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [timeFilter, setTimeFilter] = useState('30')

  useEffect(() => {
    apiRequest<Application[]>('/job-seeker/applications')
      .then(setApplications)
      .catch(() => setApplications([]))
      .finally(() => setLoading(false))
  }, [])

  const filtered = applications.filter(app => {
    if (filter === 'all') return true
    return app.status.toLowerCase() === filter.toLowerCase()
  })

  const statusColors: Record<string, string> = {
    applied: 'bg-blue-100 text-blue-700',
    screening: 'bg-yellow-100 text-yellow-700',
    interview: 'bg-purple-100 text-purple-700',
    offer: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700',
    withdrawn: 'bg-gray-100 text-gray-700',
  }

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

      {/* Filters */}
      <div className="flex gap-4">
        <select
          value={filter}
          onChange={e => setFilter(e.target.value)}
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
          onChange={e => setTimeFilter(e.target.value)}
          className="px-3 py-2 border rounded-lg text-sm"
        >
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
          <option value="all">All time</option>
        </select>
      </div>

      {/* Loading */}
      {loading && (
        <div className="text-center py-12 text-gray-500">Loading...</div>
      )}

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
          {filtered.map(app => (
            <Link
              key={app.id}
              href={`/app/applications/${app.id}`}
              className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3">
                  <span className="font-medium text-gray-900 truncate">{app.employer}</span>
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColors[app.status.toLowerCase()] || 'bg-gray-100 text-gray-600'}`}>
                    {app.status}
                  </span>
                </div>
                <div className="text-sm text-gray-500 truncate mt-0.5">{app.role}</div>
              </div>
              <div className="text-sm text-gray-400 ml-4">
                {new Date(app.applied_at).toLocaleDateString('en-SG', {
                  day: 'numeric',
                  month: 'short',
                })}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
