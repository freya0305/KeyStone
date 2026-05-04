"use client"

import { useEffect } from "react"
import { useUser } from "@clerk/nextjs"
import posthog from "posthog-js"
import { initPostHog } from "@/lib/analytics"

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  const { user } = useUser()

  useEffect(() => {
    initPostHog()
  }, [])

  // Identify user when auth state changes
  useEffect(() => {
    if (user) {
      posthog.identify(user.id, {
        email: user.emailAddresses?.[0]?.emailAddress,
        first_name: user.firstName,
      })
    }
  }, [user])

  return <>{children}</>
}
