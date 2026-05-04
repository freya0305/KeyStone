"use client"

import { useState, useEffect } from 'react'
import { apiRequest } from '@/lib/api'

export type SubscriptionTier = 'free' | 'pro'

interface SubscriptionStatus {
  tier: SubscriptionTier
  has_active_subscription: boolean
}

interface UseSubscriptionResult {
  tier: SubscriptionTier
  isPro: boolean
  isGated: boolean
  isLoading: boolean
  gatedReason: string | null
  refetch: () => void
}

const FREE_LIMIT = 3 // free analyses per month

export function useSubscription(): UseSubscriptionResult {
  const [subscription, setSubscription] = useState<SubscriptionStatus | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const fetchSubscription = () => {
    setIsLoading(true)
    apiRequest<SubscriptionStatus>('/billing/subscription')
      .then(setSubscription)
      .catch(() => setSubscription({ tier: 'free', has_active_subscription: false }))
      .finally(() => setIsLoading(false))
  }

  useEffect(() => {
    fetchSubscription()
  }, [])

  const isPro = subscription?.tier === 'pro' || subscription?.has_active_subscription

  return {
    tier: subscription?.tier ?? 'free',
    isPro,
    isGated: !isPro,
    isLoading,
    gatedReason: null,
    refetch: fetchSubscription,
  }
}

export function useRemainingAnalyses(): {
  remaining: number
  used: number
  limit: number
  isLoading: boolean
} {
  // This would ideally come from the API
  // For now, track locally - in production this would be per-user from backend
  const [count, setCount] = useState(0)
  const [isLoading, setIsLoading] = useState(false)

  return {
    remaining: Math.max(0, FREE_LIMIT - count),
    used: count,
    limit: FREE_LIMIT,
    isLoading,
  }
}
