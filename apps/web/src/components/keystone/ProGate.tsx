"use client"

import Link from 'next/link'

interface ProGateProps {
  feature: string
  section: string
  count?: number
  children: React.ReactNode
  fallback?: React.ReactNode
}

export function ProGate({ feature, section, count, children, fallback }: ProGateProps) {
  // In a real implementation, this would check the subscription tier
  // For now, we render children as-is - the actual gating happens server-side
  // This component is a placeholder for the UI treatment
  if (fallback) {
    return <>{fallback}</>
  }
  return <>{children}</>
}

interface PaywallBannerProps {
  section: string
  count: number
}

export function PaywallBanner({ section, count }: PaywallBannerProps) {
  return (
    <div className="border border-blue-200 bg-blue-50 rounded-xl p-4 my-4">
      <div className="flex items-start gap-3">
        <div className="text-blue-600 mt-0.5">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div className="flex-1">
          <p className="text-sm text-blue-900 font-medium">
            {count} more {count === 1 ? 'suggestion' : 'suggestions'} for this role
          </p>
          <p className="text-xs text-blue-700 mt-0.5">
            For your {section} — these require Pro
          </p>
        </div>
        <Link
          href="/pricing"
          className="flex-shrink-0 px-3 py-1.5 bg-blue-600 text-white text-xs font-medium rounded-lg hover:bg-blue-700"
        >
          Unlock all
        </Link>
      </div>
      <div className="mt-3 pt-3 border-t border-blue-100">
        <button
          onClick={() => {
            window.location.href = '/pricing'
          }}
          className="text-xs text-blue-600 hover:text-blue-800 underline"
        >
          Try Pro free for 3 days (no card needed)
        </button>
        <span className="text-xs text-gray-400 mx-2">or</span>
        <button
          onClick={() => {
            // Skip - move on
          }}
          className="text-xs text-gray-500 hover:text-gray-700"
        >
          Analyse a different job for free
        </button>
      </div>
    </div>
  )
}
