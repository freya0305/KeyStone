"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { apiRequest } from "@/lib/api"
import { AutoCloseBanner } from "@/components/keystone/AutoCloseBanner"

interface Application {
  id: string
  employer: string
  role: string
  status: string
  applied_at: string
  job_url?: string
}

interface AnalyticsSummary {
  total_applications: number
  by_status: Record<string, number>
  nudge_eligible_count: number
  active_last_30d: number
  completed_last_30d: number
}

interface AutoClosedApplication {
  id: string
  employer: string
  role: string
  status: string
  auto_closed_at: string
}

export default function DashboardPage() {
  const [applications, setApplications] = useState<Application[]>([])
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null)
  const [autoClosedApps, setAutoClosedApps] = useState<AutoClosedApplication[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch applications, analytics, and auto-closed in parallel
    Promise.all([
      apiRequest<Application[]>("/job-seeker/applications"),
      apiRequest<AnalyticsSummary>("/job-seeker/analytics/summary"),
      apiRequest<AutoClosedApplication[]>("/job-seeker/applications/auto-closed"),
    ])
      .then(([apps, summary, autoClosed]) => {
        setApplications(apps.slice(0, 5)) // Recent 5
        setAnalytics(summary)
        setAutoClosedApps(autoClosed)
      })
      .catch(() => {
        setApplications([])
        setAnalytics(null)
        setAutoClosedApps([])
      })
      .finally(() => setLoading(false))
  }, [])

  const statusColors: Record<string, string> = {
    applied: "bg-blue-100 text-blue-700",
    screening: "bg-yellow-100 text-yellow-700",
    interview: "bg-purple-100 text-purple-700",
    offer: "bg-green-100 text-green-700",
    rejected: "bg-red-100 text-red-700",
    withdrawn: "bg-gray-100 text-gray-700",
  }

  const recentApps = applications.slice(0, 5)

  const handleAutoClosedCorrect = (ids: string[]) => {
    // Navigate to applications page with auto-closed filter
    window.location.href = "/app/applications"
  }

  const handleAutoClosedDismiss = () => {
    // API call to acknowledge dismiss could go here
    setAutoClosedApps([])
  }

  return (
    <div className="space-y-8">
      {/* Auto-Close Banner */}
      {autoClosedApps.length > 0 && (
        <AutoCloseBanner
          applications={autoClosedApps}
          onCorrect={handleAutoClosedCorrect}
          onDismiss={handleAutoClosedDismiss}
        />
      )}

      {/* Welcome */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Welcome back</h1>
        <p className="text-gray-600">Track your job applications and get AI-powered suggestions.</p>
      </div>

      {/* Stats Cards */}
      {analytics && (
        <div className="grid md:grid-cols-4 gap-4">
          <div className="bg-white border rounded-xl p-4">
            <div className="text-2xl font-bold text-gray-900">{analytics.total_applications}</div>
            <div className="text-sm text-gray-500">Total Applications</div>
          </div>
          <div className="bg-white border rounded-xl p-4">
            <div className="text-2xl font-bold text-gray-900">{analytics.active_last_30d}</div>
            <div className="text-sm text-gray-500">Active (30d)</div>
          </div>
          <div className="bg-white border rounded-xl p-4">
            <div className="text-2xl font-bold text-green-600">{analytics.completed_last_30d}</div>
            <div className="text-sm text-gray-500">Completed (30d)</div>
          </div>
          <div className="bg-white border rounded-xl p-4">
            <div className="text-2xl font-bold text-amber-600">{analytics.nudge_eligible_count}</div>
            <div className="text-sm text-gray-500">Need Check-in</div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-4">
        <Link
          href="/app/new"
          className="p-6 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
        >
          <div className="text-2xl mb-2">+</div>
          <div className="font-semibold">New Application</div>
          <div className="text-sm text-blue-100">Track a new job opportunity</div>
        </Link>
        <Link
          href="/app/applications"
          className="p-6 bg-white border rounded-xl hover:border-gray-300 transition-colors"
        >
          <div className="text-2xl mb-2">📋</div>
          <div className="font-semibold text-gray-900">View Applications</div>
          <div className="text-sm text-gray-500">See all your tracked jobs</div>
        </Link>
        <Link
          href="/app/resumes"
          className="p-6 bg-white border rounded-xl hover:border-gray-300 transition-colors"
        >
          <div className="text-2xl mb-2">📄</div>
          <div className="font-semibold text-gray-900">Manage Resumes</div>
          <div className="text-sm text-gray-500">Upload and tailors resumes</div>
        </Link>
      </div>

      {/* Nudge Banner */}
      {analytics && analytics.nudge_eligible_count > 0 && (
        <Link
          href="/app/applications"
          className="block bg-amber-50 border border-amber-200 rounded-xl p-4 hover:bg-amber-100 transition-colors"
        >
          <div className="flex items-center justify-between">
            <div>
              <div className="font-medium text-amber-900">
                {analytics.nudge_eligible_count} application{analytics.nudge_eligible_count !== 1 ? "s" : ""} need a quick check-in
              </div>
              <div className="text-sm text-amber-700">Keep your contacts warm — takes about 30 seconds</div>
            </div>
            <div className="text-amber-600">→</div>
          </div>
        </Link>
      )}

      {/* Recent Activity */}
      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-lg">Recent Applications</h2>
          <Link href="/app/applications" className="text-sm text-blue-600 hover:underline">
            View all →
          </Link>
        </div>

        {loading && (
          <div className="text-center py-8 text-gray-500">Loading...</div>
        )}

        {!loading && recentApps.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <p>No applications yet.</p>
            <Link href="/app/new" className="text-blue-600 hover:underline mt-2 inline-block">
              Add your first application →
            </Link>
          </div>
        )}

        {!loading && recentApps.length > 0 && (
          <div className="space-y-3">
            {recentApps.map((app) => (
              <Link
                key={app.id}
                href={`/app/applications/${app.id}`}
                className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div>
                  <div className="font-medium text-gray-900">{app.employer}</div>
                  <div className="text-sm text-gray-500">{app.role}</div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColors[app.status?.toLowerCase()] || "bg-gray-100 text-gray-600"}`}>
                    {app.status}
                  </span>
                  <span className="text-sm text-gray-400">
                    {app.applied_at ? new Date(app.applied_at).toLocaleDateString("en-SG", {
                      day: "numeric",
                      month: "short",
                    }) : "—"}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Tips */}
      <div className="bg-blue-50 border border-blue-100 rounded-xl p-6">
        <h2 className="font-semibold text-blue-900 mb-2">Pro tip</h2>
        <p className="text-blue-800 text-sm">
          Tailor your resume for each application. Users who customize their resume
          per job see 40% higher callback rates.
        </p>
      </div>
    </div>
  )
}
