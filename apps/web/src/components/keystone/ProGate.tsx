"use client"

import { useEffect } from "react"
import Link from "next/link"
import { trackPaywallSeen } from "@/lib/analytics"
import { Button } from "@/components/ui/button"

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
  useEffect(() => {
    trackPaywallSeen({ section, gated_count: count })
  }, [section, count])

  return (
    <div className="border border-brand-200 bg-brand-50 dark:bg-brand-900/20 dark:border-brand-800 rounded-xl p-4 my-4">
      <div className="flex items-start gap-3">
        <div className="text-brand-600 dark:text-brand-400 mt-0.5">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div className="flex-1">
          <p className="text-sm text-brand-900 dark:text-brand-100 font-medium">
            {count} more {count === 1 ? 'suggestion' : 'suggestions'} for this role
          </p>
          <p className="text-xs text-brand-700 dark:text-brand-300 mt-0.5">
            For your {section} — these require Pro
          </p>
        </div>
        <Link href="/pricing">
          <Button size="sm" className="bg-brand-500 hover:bg-brand-600 text-white">
            Unlock all
          </Button>
        </Link>
      </div>
      <div className="mt-3 pt-3 border-t border-brand-100 dark:border-brand-800">
        <button
          onClick={() => {
            window.location.href = '/pricing'
          }}
          className="text-xs text-brand-600 dark:text-brand-400 hover:text-brand-800 dark:hover:text-brand-300 underline"
        >
          Try Pro free for 3 days (no card needed)
        </button>
        <span className="text-xs text-stone-400 mx-2">or</span>
        <button
          onClick={() => {
            // Skip - move on
          }}
          className="text-xs text-stone-500 dark:text-stone-400 hover:text-stone-700 dark:hover:text-stone-300"
        >
          Analyse a different job for free
        </button>
      </div>
    </div>
  )
}
