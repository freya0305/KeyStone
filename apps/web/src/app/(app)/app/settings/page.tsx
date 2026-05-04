"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { apiRequest, apiDownload } from "@/lib/api"

const CONSENT_TYPES = [
  {
    key: "registration",
    label: "Account Registration",
    description: "Required for account creation. You cannot use KeyStone without this consent.",
    required: true,
  },
  {
    key: "storage",
    label: "Resume & Application Storage",
    description: "Store your resume and application data so we can provide suggestions.",
    required: true,
  },
  {
    key: "ai_processing",
    label: "AI Processing",
    description: "Send your resume and job postings to Claude API for analysis. Your data is not retained by Anthropic.",
    required: true,
  },
  {
    key: "outcome_tracking",
    label: "Application Outcome Tracking",
    description: "Track application outcomes to improve suggestions over time.",
    required: true,
  },
  {
    key: "marketing",
    label: "Marketing Communications",
    description: "Receive newsletters and promotional emails about new features.",
    required: false,
  },
  {
    key: "ai_training",
    label: "AI Model Improvement",
    description: "Help us improve by allowing anonymized feedback to be used for model training.",
    required: false,
  },
]

interface ConsentState {
  [key: string]: boolean
}

interface SubscriptionStatus {
  tier: string
  has_active_subscription: boolean
}

export default function SettingsPage() {
  const [consents, setConsents] = useState<ConsentState>({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [subscription, setSubscription] = useState<SubscriptionStatus | null>(null)
  const [portalLoading, setPortalLoading] = useState(false)
  const [darkMode, setDarkMode] = useState(false)
  const [exportLoading, setExportLoading] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState(false)

  // Load dark mode preference
  useEffect(() => {
    const saved = localStorage.getItem('darkMode')
    if (saved !== null) {
      setDarkMode(saved === 'true')
    } else {
      setDarkMode(window.matchMedia('(prefers-color-scheme: dark)').matches)
    }
  }, [])

  // Apply dark mode class to html element
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('darkMode', 'true')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('darkMode', 'false')
    }
  }, [darkMode])

  useEffect(() => {
    // Load consent state and subscription in parallel
    Promise.all([
      apiRequest<{ consents: { consent_type: string; granted: boolean }[] }>('/consent'),
      apiRequest<SubscriptionStatus>('/billing/subscription').catch(() => null),
    ])
      .then(([consentData, subData]) => {
        const state: ConsentState = {}
        consentData.consents.forEach((c) => {
          state[c.consent_type] = c.granted
        })
        setConsents(state)
        setSubscription(subData)
        setLoading(false)
      })
      .catch(() => {
        const defaults: ConsentState = {}
        CONSENT_TYPES.forEach((c) => {
          defaults[c.key] = c.required
        })
        setConsents(defaults)
        setLoading(false)
      })
  }, [])

  const openBillingPortal = async () => {
    setPortalLoading(true)
    try {
      const { portal_url } = await apiRequest<{ portal_url: string }>(
        '/billing/create-portal-session',
        { method: 'POST' }
      )
      window.location.href = portal_url
    } catch {
      setError('Failed to open billing portal')
      setPortalLoading(false)
    }
  }

  const exportUserData = async () => {
    setExportLoading(true)
    try {
      const blob = await apiDownload('/users/export', { method: 'GET' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `keystone-data-export-${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch {
      setError('Failed to export data')
    } finally {
      setExportLoading(false)
    }
  }

  const deleteAccount = async () => {
    if (!deleteConfirm) {
      setDeleteConfirm(true)
      return
    }
    try {
      await apiRequest('/users/account', { method: 'DELETE' })
      // Redirect to home after deletion
      window.location.href = '/'
    } catch {
      setError('Failed to delete account')
      setDeleteConfirm(false)
    }
  }

  const updateConsent = async (key: string, value: boolean) => {
    setSaving(key)
    setError(null)
    try {
      const endpoint = value ? `/consent/${key}/grant` : `/consent/${key}/revoke`
      await apiRequest(endpoint, { method: "POST" })
      setConsents((prev) => ({ ...prev, [key]: value }))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update consent")
    } finally {
      setSaving(null)
    }
  }

  return (
    <div className="max-w-2xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600">Manage your account and preferences.</p>
      </div>

      {/* Profile */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-4">Profile</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input
              type="text"
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="Your name"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              disabled
              className="w-full px-3 py-2 border rounded-lg bg-gray-50"
              placeholder="your@email.com"
            />
          </div>
        </div>
      </div>

      {/* Consent Management */}
      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-lg">Consent Preferences</h2>
          <Link href="/trust" className="text-sm text-blue-600 hover:underline">
            Learn more
          </Link>
        </div>
        <p className="text-sm text-gray-600 mb-6">
          Under Singapore&apos;s PDPA, you have control over how we use your data.
          Required consents cannot be disabled as they are necessary for the service.
        </p>
        {loading ? (
          <div className="text-center py-8 text-gray-500">Loading...</div>
        ) : (
          <div className="space-y-4">
            {CONSENT_TYPES.map((consent) => (
              <div key={consent.key} className="flex items-start gap-4 py-4 border-b last:border-0">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h3 className="font-medium text-gray-900">{consent.label}</h3>
                    {consent.required && (
                      <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">Required</span>
                    )}
                  </div>
                  <p className="text-sm text-gray-500 mt-1">{consent.description}</p>
                </div>
                <button
                  onClick={() => !consent.required && updateConsent(consent.key, !consents[consent.key])}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    consents[consent.key] || consent.required ? "bg-blue-600" : "bg-gray-200"
                  }`}
                  disabled={consent.required || saving !== null}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      consents[consent.key] || consent.required ? "translate-x-6" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>
            ))}
          </div>
        )}
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}
      </div>

      {/* Billing */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-4">Billing</h2>
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div>
            <div className="font-medium">
              {subscription?.tier === 'pro' ? 'Pro Plan' : 'Free Plan'}
            </div>
            <div className="text-sm text-gray-500">
              {subscription?.has_active_subscription
                ? 'Active subscription'
                : '3 analyses/month'}
            </div>
          </div>
          {subscription?.has_active_subscription ? (
            <button
              onClick={openBillingPortal}
              disabled={portalLoading}
              className="px-4 py-2 border border-gray-300 text-sm rounded-lg hover:bg-gray-50 disabled:opacity-50"
            >
              {portalLoading ? 'Opening...' : 'Manage subscription'}
            </button>
          ) : (
            <a
              href="/pricing"
              className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
            >
              Upgrade to Pro
            </a>
          )}
        </div>
      </div>

      {/* Appearance */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-4">Appearance</h2>
        <div className="flex items-center justify-between">
          <div>
            <div className="font-medium">Dark mode</div>
            <div className="text-sm text-gray-500">Toggle dark theme</div>
          </div>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
              darkMode ? 'bg-blue-600' : 'bg-gray-200'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                darkMode ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>
      </div>

      {/* Data & Privacy */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-4">Data & Privacy</h2>
        <p className="text-sm text-gray-600 mb-4">
          Under PDPA, you have the right to access and export your personal data.
        </p>
        <button
          onClick={exportUserData}
          disabled={exportLoading}
          className="px-4 py-2 border border-gray-300 text-sm rounded-lg hover:bg-gray-50 disabled:opacity-50"
        >
          {exportLoading ? 'Exporting...' : 'Export all my data'}
        </button>
      </div>

      {/* Danger Zone */}
      <div className="bg-white border border-red-200 rounded-xl p-6">
        <h2 className="font-semibold text-lg mb-2 text-red-600">Danger Zone</h2>
        <p className="text-sm text-gray-600 mb-4">
          Permanently delete your account and all associated data. This action cannot be undone.
        </p>
        {deleteConfirm ? (
          <div className="space-y-2">
            <p className="text-sm font-medium text-red-600">Are you absolutely sure?</p>
            <div className="flex gap-2">
              <button
                onClick={deleteAccount}
                className="px-4 py-2 bg-red-600 text-white text-sm rounded-lg hover:bg-red-700"
              >
                Yes, delete my account
              </button>
              <button
                onClick={() => setDeleteConfirm(false)}
                className="px-4 py-2 border border-gray-300 text-sm rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <button
            onClick={() => setDeleteConfirm(true)}
            className="px-4 py-2 border border-red-300 text-red-600 text-sm rounded-lg hover:bg-red-50"
          >
            Delete account
          </button>
        )}
      </div>

      {/* PDPA Footer */}
      <div className="text-center text-sm text-gray-500">
        PDPA Compliant · Your data stays in Singapore · You can delete everything anytime
      </div>
    </div>
  )
}
