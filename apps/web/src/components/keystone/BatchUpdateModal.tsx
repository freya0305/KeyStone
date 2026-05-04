"use client"

import { useState, useCallback } from "react"
import { apiRequest } from "@/lib/api"

interface Application {
  id: string
  company: string
  role: string
  applied_at: string
  source?: string
  status: string
}

interface BatchUpdateModalProps {
  isOpen: boolean
  onClose: () => void
  applications: Application[]
}

type UpdateAction = "no_news" | "response" | "rejected" | "withdrawn" | "offer" | "advance"

export function BatchUpdateModal({
  isOpen,
  onClose,
  applications,
}: BatchUpdateModalProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [completed, setCompleted] = useState<Set<string>>(new Set())
  const [isSubmitting, setIsSubmitting] = useState(false)

  const currentApp = applications[currentIndex]
  const progress = applications.filter((app) => completed.has(app.id)).length

  const handleAction = useCallback(
    async (action: UpdateAction, metadata?: { date?: string; stage?: string }) => {
      if (!currentApp) return

      setIsSubmitting(true)

      try {
        await apiRequest(`/job-seeker/applications/${currentApp.id}/batch-update`, {
          method: "POST",
          body: {
            action,
            ...metadata,
          },
        })

        setCompleted((prev) => new Set(prev).add(currentApp.id))

        // Move to next or close
        if (currentIndex < applications.length - 1) {
          setCurrentIndex((i) => i + 1)
        } else {
          onClose()
        }
      } catch {
        // Show error but allow retry
        alert("Failed to update. Please try again.")
      } finally {
        setIsSubmitting(false)
      }
    },
    [currentApp, currentIndex, applications.length, onClose]
  )

  const handleMarkAllNoNews = useCallback(async () => {
    const remaining = applications.filter((app) => !completed.has(app.id))
    setIsSubmitting(true)

    try {
      await apiRequest("/job-seeker/applications/batch-update/mark-all-no-news", {
        method: "POST",
        body: {
          application_ids: remaining.map((app) => app.id),
        },
      })

      // Show undo toast
      const undoTimeout = setTimeout(() => {
        onClose()
      }, 3000)

      // Store timeout for potential undo
      ;(window as any).__batchUndoTimeout = undoTimeout
    } catch {
      alert("Failed to mark all as no news. Please try again.")
    } finally {
      setIsSubmitting(false)
    }
  }, [applications, completed, onClose])

  if (!isOpen || !currentApp) return null

  const timeAgo = getTimeAgo(currentApp.applied_at)

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl w-full max-w-lg mx-4 overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b flex items-center justify-between">
          <div>
            <h2 className="font-semibold">Quick check-in</h2>
            <p className="text-sm text-gray-500">
              {applications.length} application{applications.length !== 1 ? "s" : ""} · ~30 seconds
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>

        {/* Current Application Card */}
        <div className="p-4">
          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <div className="flex items-start justify-between">
              <div>
                <div className="font-medium text-gray-900">
                  {currentApp.company} · {currentApp.role}
                </div>
                <div className="text-sm text-gray-500 mt-1">
                  Applied {timeAgo}
                  {currentApp.source && ` · via ${currentApp.source}`}
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="space-y-2">
            <button
              onClick={() => handleAction("no_news")}
              disabled={isSubmitting}
              className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50"
            >
              Still no news
            </button>

            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() =>
                  handleAction("response", { date: new Date().toISOString() })
                }
                disabled={isSubmitting}
                className="py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
              >
                Got a response
              </button>
              <button
                onClick={() => handleAction("rejected")}
                disabled={isSubmitting}
                className="py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
              >
                Rejected
              </button>
            </div>

            <details className="group">
              <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700 text-center py-2">
                More options ▾
              </summary>
              <div className="mt-2 space-y-2">
                <button
                  onClick={() => handleAction("withdrawn")}
                  disabled={isSubmitting}
                  className="w-full py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  Withdrawn
                </button>
                <button
                  onClick={() => handleAction("offer")}
                  disabled={isSubmitting}
                  className="w-full py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  Got an offer 🎉
                </button>
              </div>
            </details>
          </div>
        </div>

        {/* Progress */}
        <div className="px-4 pb-4">
          <div className="flex items-center justify-between text-sm text-gray-500 mb-2">
            <span>
              {progress} of {applications.length} complete
            </span>
            <button
              onClick={handleMarkAllNoNews}
              disabled={isSubmitting}
              className="text-brand-500 hover:text-brand-600 disabled:opacity-50"
            >
              Mark all remaining as no news
            </button>
          </div>
          <div className="flex gap-1">
            {applications.map((app, i) => (
              <div
                key={app.id}
                className={`h-1 flex-1 rounded-full ${
                  completed.has(app.id)
                    ? "bg-match-strong"
                    : i === currentIndex
                    ? "bg-brand-500"
                    : "bg-gray-200"
                }`}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

function getTimeAgo(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = Math.floor(
    (now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24)
  )

  if (diffDays === 0) return "today"
  if (diffDays === 1) return "yesterday"
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return `${Math.floor(diffDays / 30)} months ago`
}
