"use client"

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { apiRequest } from '@/lib/api'
import { trackApplicationCreated } from '@/lib/analytics'

type ApplicationStatus = 'applied' | 'screening' | 'interview' | 'offer' | 'rejected' | 'withdrawn'

interface ApplicationForm {
  company: string
  role: string
  job_url: string
  applied_at: string
  status: ApplicationStatus
  notes: string
}

export default function NewApplicationPage() {
  const router = useRouter()
  const [step, setStep] = useState(1)
  const [jobUrl, setJobUrl] = useState('')
  const [jobText, setJobText] = useState('')
  const [mode, setMode] = useState<'url' | 'text'>('url')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [form, setForm] = useState<ApplicationForm>({
    company: '',
    role: '',
    job_url: '',
    applied_at: new Date().toISOString().split('T')[0],
    status: 'applied',
    notes: '',
  })

  const handleNextFromStep1 = () => {
    if (mode === 'url' && !jobUrl.trim()) return
    if (mode === 'text' && !jobText.trim()) return
    setStep(2)
  }

  const handleSubmit = async () => {
    if (!form.company.trim() || !form.role.trim()) {
      setError('Company and role are required')
      return
    }
    setLoading(true)
    setError(null)
    try {
      await apiRequest<{ id: string }>('/job-seeker/applications', {
        method: 'POST',
        body: {
          ...form,
          applied_at: new Date(form.applied_at).toISOString(),
        },
      })

      // Track application_created
      trackApplicationCreated({
        from_download: false,
        employer: form.company,
      })

      router.push('/app/applications')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create application')
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">New Application</h1>
        <p className="text-gray-600">Track a new job opportunity.</p>
      </div>

      {/* Steps */}
      <div className="flex items-center gap-2">
        {[1, 2, 3].map(s => (
          <div key={s} className="flex items-center gap-2">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                step >= s ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'
              }`}
            >
              {s}
            </div>
            {s < 3 && (
              <div className={`w-12 h-0.5 ${step > s ? 'bg-blue-600' : 'bg-gray-200'}`} />
            )}
          </div>
        ))}
      </div>

      {/* Step 1: Job Details */}
      {step === 1 && (
        <div className="bg-white border rounded-xl p-6 space-y-6">
          <h2 className="font-semibold text-lg">Where are you applying?</h2>

          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => { setMode('url'); setJobText('') }}
              className={`flex-1 p-4 border rounded-lg text-center transition-colors ${
                mode === 'url' ? 'border-blue-500 bg-blue-50' : 'hover:border-gray-300'
              }`}
            >
              <div className="text-2xl mb-2">🔗</div>
              <div className="font-medium">Job URL</div>
              <div className="text-sm text-gray-500">Paste from MyCareersFuture, etc.</div>
            </button>
            <button
              type="button"
              onClick={() => { setMode('text'); setJobUrl('') }}
              className={`flex-1 p-4 border rounded-lg text-center transition-colors ${
                mode === 'text' ? 'border-blue-500 bg-blue-50' : 'hover:border-gray-300'
              }`}
            >
              <div className="text-2xl mb-2">📋</div>
              <div className="font-medium">Paste Text</div>
              <div className="text-sm text-gray-500">Copy job description directly</div>
            </button>
          </div>

          {mode === 'url' ? (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Job Posting URL</label>
              <input
                type="url"
                value={jobUrl}
                onChange={e => setJobUrl(e.target.value)}
                placeholder="https://..."
                className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          ) : (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Job Description</label>
              <textarea
                value={jobText}
                onChange={e => setJobText(e.target.value)}
                rows={8}
                placeholder="Paste job description here..."
                className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          )}

          <div className="flex justify-between">
            <Link href="/app" className="px-4 py-2 text-gray-600 hover:text-gray-900">
              Cancel
            </Link>
            <button
              type="button"
              onClick={handleNextFromStep1}
              disabled={mode === 'url' ? !jobUrl.trim() : !jobText.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              Continue
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Company Info */}
      {step === 2 && (
        <div className="bg-white border rounded-xl p-6 space-y-6">
          <h2 className="font-semibold text-lg">Company & Role</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Company Name *</label>
              <input
                type="text"
                value={form.company}
                onChange={e => setForm(f => ({ ...f, company: e.target.value }))}
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="e.g. DBS Bank"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Role / Position *</label>
              <input
                type="text"
                value={form.role}
                onChange={e => setForm(f => ({ ...f, role: e.target.value }))}
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="e.g. Software Engineer"
              />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Applied Date</label>
              <input
                type="date"
                value={form.applied_at}
                onChange={e => setForm(f => ({ ...f, applied_at: e.target.value }))}
                className="w-full px-3 py-2 border rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={form.status}
                onChange={e => setForm(f => ({ ...f, status: e.target.value as ApplicationStatus }))}
                className="w-full px-3 py-2 border rounded-lg"
              >
                <option value="applied">Applied</option>
                <option value="screening">Screening</option>
                <option value="interview">Interview</option>
                <option value="offer">Offer</option>
                <option value="rejected">Rejected</option>
                <option value="withdrawn">Withdrawn</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
            <textarea
              value={form.notes}
              onChange={e => setForm(f => ({ ...f, notes: e.target.value }))}
              rows={3}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="Any notes about this application..."
            />
          </div>
          <div className="flex justify-between">
            <button
              type="button"
              onClick={() => setStep(1)}
              className="px-4 py-2 text-gray-600 hover:text-gray-900"
            >
              Back
            </button>
            <button
              type="button"
              onClick={() => setStep(3)}
              disabled={!form.company.trim() || !form.role.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              Continue
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Confirmation */}
      {step === 3 && (
        <div className="bg-white border rounded-xl p-6 space-y-6">
          <h2 className="font-semibold text-lg">Ready to track</h2>
          <div className="p-4 bg-gray-50 rounded-lg space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Company</span>
              <span className="font-medium">{form.company}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Role</span>
              <span className="font-medium">{form.role}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Status</span>
              <span className="font-medium capitalize">{form.status}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Applied</span>
              <span className="font-medium">
                {new Date(form.applied_at).toLocaleDateString('en-SG', {
                  day: 'numeric',
                  month: 'long',
                  year: 'numeric',
                })}
              </span>
            </div>
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div className="flex justify-between">
            <button
              type="button"
              onClick={() => setStep(2)}
              className="px-4 py-2 text-gray-600 hover:text-gray-900"
            >
              Back
            </button>
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save Application'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
