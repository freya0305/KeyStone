"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useUser } from '@clerk/nextjs'
import { apiRequest } from '@/lib/api'
import { trackProSubscribed } from '@/lib/analytics'

type Plan = 'monthly' | 'annual'

interface SubscriptionStatus {
  tier: string
  has_active_subscription: boolean
}

export default function PricingPage() {
  const { user, isLoaded } = useUser()
  const [plan, setPlan] = useState<Plan>('monthly')
  const [subscription, setSubscription] = useState<SubscriptionStatus | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!user) return
    apiRequest<SubscriptionStatus>('/billing/subscription')
      .then(setSubscription)
      .catch(() => setSubscription(null))
  }, [user])

  const handleSubscribe = async () => {
    if (!user) {
      window.location.href = '/sign-up?plan=pro'
      return
    }
    setLoading(true)
    setError(null)
    try {
      const { checkout_url } = await apiRequest<{ checkout_url: string }>(
        '/billing/create-checkout-session',
        { method: 'POST', body: { plan } }
      )

      // Track pro_subscribed event
      trackProSubscribed({ plan })

      window.location.href = checkout_url
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start checkout')
      setLoading(false)
    }
  }

  const handleTrial = async () => {
    if (!user) {
      window.location.href = '/sign-up?plan=pro'
      return
    }
    setLoading(true)
    setError(null)
    try {
      const { checkout_url } = await apiRequest<{ checkout_url: string }>(
        '/billing/create-trial',
        { method: 'POST' }
      )
      window.location.href = checkout_url
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start trial')
      setLoading(false)
    }
  }

  const isPro = subscription?.tier === 'pro' || subscription?.has_active_subscription

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">KS</span>
            </div>
            <span className="font-semibold text-xl">KeyStone</span>
          </Link>
          <Link
            href={user ? '/app/settings' : '/sign-in'}
            className="text-sm text-gray-600 hover:text-gray-900"
          >
            {user ? 'Settings' : 'Sign in'}
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Simple, transparent pricing
          </h1>
          <p className="text-gray-600">
            Start free. Upgrade when you&apos;re ready to land your dream job.
          </p>
        </div>

        {/* Plan toggle */}
        {!isPro && (
          <div className="flex justify-center mb-8">
            <div className="inline-flex rounded-lg border bg-white p-1">
              <button
                onClick={() => setPlan('monthly')}
                className={`px-4 py-2 text-sm rounded-md transition-colors ${
                  plan === 'monthly'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setPlan('annual')}
                className={`px-4 py-2 text-sm rounded-md transition-colors ${
                  plan === 'annual'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Annual
                <span className="ml-1 text-xs text-green-600 font-medium">Save 2 months</span>
              </button>
            </div>
          </div>
        )}

        {error && (
          <div className="max-w-md mx-auto mb-6 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm text-center">
            {error}
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-8 max-w-3xl mx-auto">
          {/* Free Tier */}
          <div className="bg-white border rounded-xl p-8">
            <h2 className="text-xl font-bold text-gray-900 mb-2">Free</h2>
            <div className="mb-6">
              <span className="text-4xl font-bold text-gray-900">SGD 0</span>
              <span className="text-gray-500">/month</span>
            </div>
            <p className="text-gray-600 mb-6">
              Perfect for trying KeyStone and occasional applications.
            </p>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                3 job analyses/month
              </li>
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                3 AI suggestions/month
              </li>
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Resume upload
              </li>
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Application tracking
              </li>
              <li className="flex items-center gap-2 text-sm text-gray-400">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                Unlimited suggestions
              </li>
              <li className="flex items-center gap-2 text-sm text-gray-400">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                Insights dashboard
              </li>
            </ul>
            <Link
              href={user ? '/app' : '/sign-up'}
              className="block w-full py-3 text-center border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              {user ? 'Go to dashboard' : 'Get started free'}
            </Link>
          </div>

          {/* Pro Tier */}
          <div className="bg-blue-600 text-white rounded-xl p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 bg-yellow-400 text-yellow-900 text-xs font-bold px-3 py-1 rounded-bl-lg">
              RECOMMENDED
            </div>
            <h2 className="text-xl font-bold mb-2">Pro</h2>
            <div className="mb-6">
              {plan === 'monthly' ? (
                <>
                  <span className="text-4xl font-bold">SGD 19</span>
                  <span className="text-blue-200">/month</span>
                </>
              ) : (
                <>
                  <span className="text-4xl font-bold">SGD 190</span>
                  <span className="text-blue-200">/year</span>
                </>
              )}
            </div>
            <p className="text-blue-100 mb-6">
              For serious job seekers who want every advantage.
            </p>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <strong>Unlimited</strong> job analyses
              </li>
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <strong>Unlimited</strong> AI suggestions
              </li>
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Resume upload & versioning
              </li>
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Full application tracking
              </li>
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Insights dashboard
              </li>
              <li className="flex items-center gap-2 text-sm">
                <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Callback rate analytics
              </li>
            </ul>

            {isPro ? (
              <Link
                href="/app/settings"
                className="block w-full py-3 text-center bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors"
              >
                Manage subscription
              </Link>
            ) : isLoaded && user ? (
              <>
                <button
                  onClick={handleSubscribe}
                  disabled={loading}
                  className="block w-full py-3 text-center bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Redirecting...' : `Start Pro — ${plan === 'monthly' ? 'SGD 19/month' : 'SGD 190/year'}`}
                </button>
                <button
                  onClick={handleTrial}
                  disabled={loading}
                  className="block w-full py-2 text-center text-blue-200 text-sm mt-2 hover:text-white transition-colors disabled:opacity-50"
                >
                  Try free for 3 days (no card needed)
                </button>
              </>
            ) : (
              <Link
                href="/sign-up?plan=pro"
                className="block w-full py-3 text-center bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors"
              >
                Start free trial
              </Link>
            )}
          </div>
        </div>

        {/* Tax note */}
        <p className="text-center text-sm text-gray-500 mt-6">
          Prices exclude 9% GST
        </p>

        {/* FAQ */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-center mb-8">Common questions</h2>
          <div className="grid md:grid-cols-2 gap-6 max-w-3xl mx-auto">
            <div>
              <h3 className="font-semibold mb-2">Can I cancel anytime?</h3>
              <p className="text-sm text-gray-600">
                Yes, cancel anytime from your settings. You&apos;ll keep Pro access until the end of your billing period.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">What counts as a job analysis?</h3>
              <p className="text-sm text-gray-600">
                An analysis is when you submit a job posting and KeyStone analyses how well your resume fits. Free users get 3 per month.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">Is my data secure?</h3>
              <p className="text-sm text-gray-600">
                Yes. We&apos;re PDPA compliant. Your resume is stored in Singapore. NRIC numbers are automatically detected and masked.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">What about B2B / recruiters?</h3>
              <p className="text-sm text-gray-600">
                Recruiter pricing is different. <Link href="/recruiter" className="text-blue-600 hover:underline">Contact us</Link> for team pricing and white-label options.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
