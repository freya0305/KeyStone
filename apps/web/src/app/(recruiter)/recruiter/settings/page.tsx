"use client"

import { useState } from "react"

export default function RecruiterSettingsPage() {
  const [company, setCompany] = useState({
    name: "",
    website: "",
    industry: "",
    description: "",
  })
  const [teamMembers] = useState<string[]>([])

  return (
    <div className="max-w-2xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600">Manage your recruiter account and team.</p>
      </div>

      {/* Company Profile */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-4">Company Profile</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
            <input
              type="text"
              value={company.name}
              onChange={e => setCompany(c => ({ ...c, name: e.target.value }))}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="Your company name"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Website</label>
            <input
              type="url"
              value={company.website}
              onChange={e => setCompany(c => ({ ...c, website: e.target.value }))}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="https://..."
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
            <select
              value={company.industry}
              onChange={e => setCompany(c => ({ ...c, industry: e.target.value }))}
              className="w-full px-3 py-2 border rounded-lg"
            >
              <option value="">Select industry...</option>
              <option value="banking">Banking & Finance</option>
              <option value="fintech">Fintech</option>
              <option value="technology">Technology</option>
              <option value="healthcare">Healthcare</option>
              <option value="retail">Retail</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              value={company.description}
              onChange={e => setCompany(c => ({ ...c, description: e.target.value }))}
              rows={3}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="Brief description of your company"
            />
          </div>
          <button className="px-4 py-2 bg-purple-600 text-white text-sm rounded-lg hover:bg-purple-700">
            Save Changes
          </button>
        </div>
      </div>

      {/* Team Management */}
      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-lg">Team Members</h2>
          <button className="px-4 py-2 bg-purple-600 text-white text-sm rounded-lg hover:bg-purple-700">
            Invite Member
          </button>
        </div>

        {teamMembers.length > 0 ? (
          <div className="space-y-3">
            {teamMembers.map(member => (
              <div key={member} className="flex items-center justify-between py-3 border-b last:border-0">
                <span className="text-gray-900">{member}</span>
                <button className="text-sm text-red-600 hover:text-red-700">Remove</button>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-sm">No team members yet. Invite your first colleague.</p>
        )}
      </div>

      {/* Billing */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-4">Billing</h2>
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div>
            <div className="font-medium">Recruiter Plan</div>
            <div className="text-sm text-gray-500">Custom pricing based on team size</div>
          </div>
          <a
            href="mailto:billing@keystone.sg?subject=Recruiter%20Billing%20Inquiry"
            className="px-4 py-2 border text-sm rounded-lg hover:bg-gray-50"
          >
            Contact us
          </a>
        </div>
      </div>

      {/* Privacy */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-4">Privacy & Data</h2>
        <p className="text-sm text-gray-600 mb-4">
          Your job descriptions and candidate data are processed in accordance with Singapore&apos;s PDPA.
          KeyStone does not use your data for AI training without explicit consent.
        </p>
        <div className="space-y-3">
          <label className="flex items-center gap-3">
            <input type="checkbox" defaultChecked className="w-4 h-4 text-purple-600 rounded" />
            <span className="text-sm text-gray-700">
              Allow anonymized usage data to improve KeyStone services
            </span>
          </label>
          <label className="flex items-center gap-3">
            <input type="checkbox" className="w-4 h-4 text-purple-600 rounded" />
            <span className="text-sm text-gray-700">
              Receive product updates and tips via email
            </span>
          </label>
        </div>
      </div>
    </div>
  )
}
