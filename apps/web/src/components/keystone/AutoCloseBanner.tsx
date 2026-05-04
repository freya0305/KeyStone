"use client"

import { useState } from "react"

interface AutoClosedApplication {
  id: string
  employer: string
  role: string
  status: string
  auto_closed_at: string
}

interface AutoCloseBannerProps {
  applications: AutoClosedApplication[]
  onCorrect: (ids: string[]) => void
  onDismiss: () => void
}

export function AutoCloseBanner({
  applications,
  onCorrect,
  onDismiss,
}: AutoCloseBannerProps) {
  const [isVisible, setIsVisible] = useState(true)

  if (!isVisible || applications.length === 0) return null

  const handleCorrect = () => {
    onCorrect(applications.map((app) => app.id))
  }

  const handleDismiss = () => {
    setIsVisible(false)
    onDismiss()
  }

  return (
    <div className="bg-brand-50 dark:bg-brand-900/20 border border-brand-200 dark:border-brand-800 rounded-xl p-4 mb-6">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 bg-brand-100 dark:bg-brand-900 rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-brand-600 dark:text-brand-400">ⓘ</span>
        </div>
        <div className="flex-1">
          <div className="font-medium text-brand-900 dark:text-brand-100">
            {applications.length} application
            {applications.length !== 1 ? "s" : ""} auto-closed (30 days, no response)
          </div>
          <div className="text-sm text-brand-700 dark:text-brand-300 mt-1">
            {applications.map((app) => app.employer).join(" · ")}
          </div>
          <div className="flex gap-2 mt-3">
            <button
              onClick={handleCorrect}
              className="px-3 py-1.5 bg-brand-500 text-white text-sm rounded-lg hover:bg-brand-600"
            >
              Correct
            </button>
            <button
              onClick={handleDismiss}
              className="px-3 py-1.5 bg-white dark:bg-stone-800 border border-brand-300 dark:border-brand-700 text-brand-700 dark:text-brand-300 text-sm rounded-lg hover:bg-brand-50 dark:hover:bg-brand-900/40"
            >
              Looks right
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
