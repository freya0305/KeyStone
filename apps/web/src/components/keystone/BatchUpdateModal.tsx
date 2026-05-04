"use client"

import { useState, useCallback, useEffect, useRef } from "react"
import { apiRequest } from "@/lib/api"
import posthog from "posthog-js"

interface Application {
  id: string
  employer: string
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
  const [undoToast, setUndoToast] = useState<{
    message: string
    undoAction: () => void
  } | null>(null)
  const [exitingId, setExitingId] = useState<string | null>(null)

  // Refs to hold latest values for keyboard handler
  const currentIndexRef = useRef(currentIndex)
  const currentAppRef = useRef(applications[0])
  const completedRef = useRef(completed)
  const applicationsLengthRef = useRef(applications.length)
  const onCloseRef = useRef(onClose)

  useEffect(() => {
    currentIndexRef.current = currentIndex
    currentAppRef.current = applications[currentIndex]
    completedRef.current = completed
    applicationsLengthRef.current = applications.length
    onCloseRef.current = onClose
  }, [currentIndex, applications, completed, onClose])

  const handleAction = useCallback(
    async (action: UpdateAction, metadata?: { date?: string; stage?: string }) => {
      const app = currentAppRef.current
      if (!app) return

      setIsSubmitting(true)

      try {
        const statusMap: Record<UpdateAction, { status?: string; final_outcome?: string }> = {
          no_news: { status: "applied" },
          response: { status: "screening" },
          rejected: { status: "rejected", final_outcome: "rejected" },
          withdrawn: { status: "withdrawn", final_outcome: "withdrawn" },
          offer: { status: "offer", final_outcome: "offer" },
          advance: { status: "interview" },
        }

        const update = statusMap[action] || { status: "applied" }

        await apiRequest("/job-seeker/applications/batch-update", {
          method: "POST",
          body: {
            applications: [
              {
                id: app.id,
                status: update.status,
                final_outcome: update.final_outcome,
              },
            ],
          },
        })

        // Animate card exit
        setExitingId(app.id)

        // Small delay for animation before state update
        await new Promise((resolve) => setTimeout(resolve, 200))

        setCompleted((prev) => new Set(prev).add(app.id))

        const nextIndex = currentIndexRef.current + 1
        if (nextIndex < applicationsLengthRef.current) {
          setCurrentIndex(nextIndex)
        } else {
          onCloseRef.current()
        }
      } catch {
        alert("Failed to update. Please try again.")
      } finally {
        setIsSubmitting(false)
        setExitingId(null)
      }
    },
    []
  )

  const handleMarkAllNoNews = useCallback(async () => {
    setIsSubmitting(true)

    try {
      // Mark all remaining as no news
      const remainingApps = applications.filter((app) => !completedRef.current.has(app.id))
      const undoData = remainingApps.map((app) => ({ id: app.id, status: app.status }))

      await apiRequest("/job-seeker/applications/mark-all-no-news", {
        method: "POST",
      })

      // Track batch_update event with metrics
      posthog.capture("batch_update", {
        action: "mark_all_no_news",
        applications_count: remainingApps.length,
        source: "BatchUpdateModal",
      })

      // Show undo toast
      setUndoToast({
        message: `${remainingApps.length} application${remainingApps.length !== 1 ? "s" : ""} marked as no news`,
        undoAction: async () => {
          // Revert: submit original statuses
          for (const app of undoData) {
            await apiRequest("/job-seeker/applications/batch-update", {
              method: "POST",
              body: {
                applications: [{ id: app.id, status: app.status }],
              },
            })
          }
          setCompleted(new Set())
          setCurrentIndex(0)
        },
      })

      // Auto-dismiss toast after 8 seconds
      setTimeout(() => {
        setUndoToast(null)
        onCloseRef.current()
      }, 8000)
    } catch {
      alert("Failed to mark all as no news. Please try again.")
    } finally {
      setIsSubmitting(false)
    }
  }, [])

  // Keyboard shortcuts
  useEffect(() => {
    if (!isOpen) return

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return

      switch (e.key) {
        case " ":
        case "Enter":
          e.preventDefault()
          handleAction("no_news")
          break
        case "r":
        case "R":
          e.preventDefault()
          handleAction("response", { date: new Date().toISOString() })
          break
        case "x":
        case "X":
          e.preventDefault()
          handleAction("rejected")
          break
        case "Escape":
          e.preventDefault()
          onClose()
          break
      }
    }

    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [isOpen, handleAction, onClose])

  // Cleanup timeouts on unmount
  useEffect(() => {
    return () => {
      if (undoToast) {
        // Component unmounting with toast showing
      }
    }
  }, [])

  if (!isOpen) return null

  const currentApp = applications[currentIndex]
  const progress = applications.filter((app) => completed.has(app.id)).length

  if (!currentApp) return null

  const timeAgo = getTimeAgo(currentApp.applied_at)

  return (
    <>
      {/* Undo Toast */}
      {undoToast && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100]">
          <div className="bg-gray-900 text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-4">
            <span>{undoToast.message}</span>
            <button
              onClick={() => {
                undoToast.undoAction()
                setUndoToast(null)
              }}
              className="px-3 py-1 bg-white text-gray-900 rounded text-sm font-medium hover:bg-gray-100"
            >
              Undo
            </button>
            <button
              onClick={() => setUndoToast(null)}
              className="text-gray-400 hover:text-white ml-2"
            >
              ✕
            </button>
          </div>
        </div>
      )}

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
            <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
              ✕
            </button>
          </div>

          {/* Keyboard hint */}
          <div className="px-4 pt-2 text-xs text-gray-400 text-center">
            Space = no news · R = response · X = rejected · Esc = close
          </div>

          {/* Current Application Card */}
          <div className="p-4">
            <div
              className={`bg-gray-50 rounded-lg p-4 mb-4 transition-all duration-200 ${
                exitingId === currentApp.id ? "opacity-0 -translate-x-8" : "opacity-100 translate-x-0"
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="font-medium text-gray-900">
                    {currentApp.employer} · {currentApp.role}
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
                  onClick={() => handleAction("response", { date: new Date().toISOString() })}
                  disabled={isSubmitting}
                  className="py-2 border border-stone-200 dark:border-stone-700 rounded-lg hover:bg-stone-50 dark:hover:bg-stone-800 disabled:opacity-50"
                >
                  Got a response
                </button>
                <button
                  onClick={() => handleAction("rejected")}
                  disabled={isSubmitting}
                  className="py-2 border border-stone-200 dark:border-stone-700 rounded-lg hover:bg-stone-50 dark:hover:bg-stone-800 disabled:opacity-50"
                >
                  Rejected
                </button>
              </div>

              <details className="group">
                <summary className="cursor-pointer text-sm text-stone-500 dark:text-stone-400 hover:text-stone-700 dark:hover:text-stone-200 text-center py-2">
                  More options ▾
                </summary>
                <div className="mt-2 space-y-2">
                  <button
                    onClick={() => handleAction("withdrawn")}
                    disabled={isSubmitting}
                    className="w-full py-2 border border-stone-200 dark:border-stone-700 rounded-lg hover:bg-stone-50 dark:hover:bg-stone-800 disabled:opacity-50"
                  >
                    Withdrawn
                  </button>
                  <button
                    onClick={() => handleAction("offer")}
                    disabled={isSubmitting}
                    className="w-full py-2 border border-stone-200 dark:border-stone-700 rounded-lg hover:bg-stone-50 dark:hover:bg-stone-800 disabled:opacity-50"
                  >
                    Got an offer 🎉
                  </button>
                </div>
              </details>
            </div>
          </div>

          {/* Progress */}
          <div className="px-4 pb-4">
            <div className="flex items-center justify-between text-sm text-stone-500 dark:text-stone-400 mb-2">
              <span>
                {progress} of {applications.length} complete
              </span>
              <button
                onClick={handleMarkAllNoNews}
                disabled={isSubmitting}
                className="text-brand-500 hover:text-brand-600 dark:text-brand-400 dark:hover:text-brand-300 disabled:opacity-50"
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
                      : "bg-stone-200 dark:bg-stone-700"
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

function getTimeAgo(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return "today"
  if (diffDays === 1) return "yesterday"
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return `${Math.floor(diffDays / 30)} months ago`
}
