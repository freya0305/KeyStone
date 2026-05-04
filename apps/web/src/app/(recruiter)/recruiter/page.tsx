import Link from "next/link"

export default function RecruiterDashboardPage() {
  return (
    <div className="space-y-8">
      {/* Welcome */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Recruiter Dashboard</h1>
        <p className="text-gray-600">Generate and manage job descriptions with AI.</p>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-4">
        <Link
          href="/recruiter/jd"
          className="p-6 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition-colors"
        >
          <div className="text-2xl mb-2">+</div>
          <div className="font-semibold">New Job Description</div>
          <div className="text-sm text-purple-100">Generate with AI</div>
        </Link>
        <Link
          href="/recruiter/templates"
          className="p-6 bg-white border rounded-xl hover:border-gray-300 transition-colors"
        >
          <div className="text-2xl mb-2">📝</div>
          <div className="font-semibold text-gray-900">Templates</div>
          <div className="text-sm text-gray-500">Manage brand templates</div>
        </Link>
        <Link
          href="/recruiter/team"
          className="p-6 bg-white border rounded-xl hover:border-gray-300 transition-colors"
        >
          <div className="text-2xl mb-2">👥</div>
          <div className="font-semibold text-gray-900">Team</div>
          <div className="text-sm text-gray-500">Invite team members</div>
        </Link>
      </div>

      {/* Recent JDs */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-4">Recent Job Descriptions</h2>
        <div className="text-center py-12 text-gray-500">
          <p>No job descriptions yet.</p>
          <Link href="/recruiter/jd" className="text-purple-600 hover:underline mt-2 inline-block">
            Create your first JD →
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid md:grid-cols-4 gap-4">
        <div className="bg-white border rounded-xl p-4">
          <div className="text-2xl font-bold text-gray-900">0</div>
          <div className="text-sm text-gray-500">Job Descriptions</div>
        </div>
        <div className="bg-white border rounded-xl p-4">
          <div className="text-2xl font-bold text-gray-900">0</div>
          <div className="text-sm text-gray-500">Share Links</div>
        </div>
        <div className="bg-white border rounded-xl p-4">
          <div className="text-2xl font-bold text-gray-900">0</div>
          <div className="text-sm text-gray-500">Team Members</div>
        </div>
        <div className="bg-white border rounded-xl p-4">
          <div className="text-2xl font-bold text-gray-900">0</div>
          <div className="text-sm text-gray-500">Seats Used</div>
        </div>
      </div>
    </div>
  )
}
