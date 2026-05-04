"use client"

import { useState } from "react"

interface AutoClosedApplication {
  id: string
  company: string
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
    <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-blue-600">ⓘ</span>
        </div>
        <div className="flex-1">
          <div className="font-medium text-blue-900">
            {applications.length} application
            {applications.length !== 1 ? "s" : ""} auto-closed (30 days, no response)
          </div>
          <div className="text-sm text-blue-700 mt-1">
            {applications.map((app) => app.company).join(" · ")}
          </div>
          <div className="flex gap-2 mt-3">
            <button
              onClick={handleCorrect}
              className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
            >
              Correct
            </button>
            <button
              onClick={handleDismiss}
              className="px-3 py-1.5 bg-white border border-blue-300 text-blue-700 text-sm rounded-lg hover:bg-blue-50"
            >
              Looks right
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
