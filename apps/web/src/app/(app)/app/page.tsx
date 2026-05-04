import Link from "next/link"
import { auth } from "@clerk/nextjs"

export default async function DashboardPage() {
  const { userId } = auth()

  return (
    <div className="space-y-8">
      {/* Welcome */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Welcome back</h1>
        <p className="text-gray-600">Track your job applications and get AI-powered suggestions.</p>
      </div>

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

      {/* Recent Activity */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-4">Recent Applications</h2>
        <div className="text-center py-12 text-gray-500">
          <p>No applications yet.</p>
          <Link href="/app/new" className="text-blue-600 hover:underline mt-2 inline-block">
            Add your first application →
          </Link>
        </div>
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
