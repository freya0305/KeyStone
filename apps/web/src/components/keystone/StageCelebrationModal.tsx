"use client"

import { useState, useEffect, useCallback } from "react"
import { apiRequest } from "@/lib/api"

interface Application {
  id: string
  employer: string
  role: string
}

interface StageCelebrationModalProps {
  isOpen: boolean
  onClose: () => void
  application: Application | null
  isOffer?: boolean
}

const STAGE_FORMATS = [
  { value: "phone", label: "Phone" },
  { value: "video", label: "Video" },
  { value: "in-person", label: "In-person" },
  { value: "panel", label: "Panel" },
  { value: "technical", label: "Technical" },
  { value: "case", label: "Case study" },
  { value: "assessment_centre", label: "Assessment Centre" },
]

export function StageCelebrationModal({
  isOpen,
  onClose,
  application,
  isOffer = false,
}: StageCelebrationModalProps) {
  const [showCelebration, setShowCelebration] = useState(false)
  const [confettiPieces, setConfettiPieces] = useState<Array<{ id: number; x: number; color: string; delay: number }>>([])
  const [selectedFormat, setSelectedFormat] = useState<string>("")
  const [nextRoundDate, setNextRoundDate] = useState<string>("")
  const [reflectionChecked, setReflectionChecked] = useState<Record<string, boolean>>({})
  const [reflectionText, setReflectionText] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const celebrationDuration = isOffer ? 2400 : 1200
  const brandColors = ["#2563eb", "#7c3aed", "#059669", "#d97706", "#dc2626"]

  const launchConfetti = useCallback(() => {
    const pieces = Array.from({ length: 12 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      color: brandColors[i % brandColors.length],
      delay: Math.random() * 0.3,
    }))
    setConfettiPieces(pieces)
    setTimeout(() => setConfettiPieces([]), celebrationDuration)
  }, [celebrationDuration, brandColors])

  const handleAdvanceStage = useCallback(
    async (stageType: string, outcome: string = "pending") => {
      if (!application) return

      setIsSubmitting(true)
      try {
        await apiRequest(`/job-seeker/applications/${application.id}/stages`, {
          method: "POST",
          body: {
            stage_type: stageType,
            round_number: stageType === "interview" ? 1 : undefined,
            format: selectedFormat || undefined,
            outcome,
            stage_date: nextRoundDate || undefined,
          },
        })
        onClose()
      } catch (err) {
        console.error("Failed to record stage:", err)
      } finally {
        setIsSubmitting(false)
      }
    },
    [application, selectedFormat, nextRoundDate, onClose]
  )

  const handleOfferCelebrate = useCallback(async () => {
    if (!application) return

    setIsSubmitting(true)
    try {
      // Record the offer stage
      await apiRequest(`/job-seeker/applications/${application.id}/stages`, {
        method: "POST",
        body: {
          stage_type: "offer",
          outcome: "pending",
          notes: `Reflection: ${Object.entries(reflectionChecked)
            .filter(([, v]) => v)
            .map(([k]) => k)
            .join(", ")}${reflectionText ? `. Additional: ${reflectionText}` : ""}`,
        },
      })
      setShowCelebration(true)
      launchConfetti()
    } catch (err) {
      console.error("Failed to record offer:", err)
    } finally {
      setIsSubmitting(false)
    }
  }, [application, reflectionChecked, reflectionText, launchConfetti])

  if (!isOpen || !application) return null

  // Celebration screen
  if (showCelebration) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl w-full max-w-md mx-4 p-8 text-center relative overflow-hidden">
          {/* Confetti */}
          {confettiPieces.map((piece) => (
            <div
              key={piece.id}
              className="absolute w-3 h-3 rounded-sm"
              style={{
                left: `${piece.x}%`,
                top: "-20px",
                backgroundColor: piece.color,
                animation: `confetti-fall ${celebrationDuration}ms ease-out ${piece.delay}s forwards`,
              }}
            />
          ))}

          <style jsx>{`
            @keyframes confetti-fall {
              0% {
                transform: translateY(0) rotate(0deg);
                opacity: 1;
              }
              100% {
                transform: translateY(400px) rotate(720deg);
                opacity: 0;
              }
            }
          `}</style>

          <div className="relative z-10">
            <div className="text-5xl mb-4">{isOffer ? "🎉" : "✨"}</div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">
              {isOffer
                ? `You got an offer at ${application.employer}!`
                : `You're advancing at ${application.employer}!`}
            </h2>
            <p className="text-gray-600 mb-6">
              {isOffer
                ? "Congratulations! This is a huge milestone."
                : `You're moving forward in the hiring process.`}
            </p>
            <div className="space-y-2">
              <button
                onClick={() => {
                  setShowCelebration(false)
                  onClose()
                }}
                className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600"
              >
                {isOffer ? "Record offer details" : "Maybe later"}
              </button>
              {!isOffer && (
                <button className="w-full py-3 border rounded-lg hover:bg-gray-50">
                  Prepare for next round →
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Advancement form
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl w-full max-w-lg mx-4 overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b">
          <h2 className="font-semibold">
            {application.employer} · {application.role}
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            {isOffer ? "Offer received! 🎉" : "What just happened?"}
          </p>
        </div>

        <div className="p-4 space-y-4">
          {/* Stage options for advancement */}
          {!isOffer && (
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">
                Stage passed
              </label>
              <div className="grid grid-cols-2 gap-2">
                {["response", "screening", "interview", "final"].map((stage) => (
                  <button
                    key={stage}
                    onClick={() => handleAdvanceStage(stage, "passed")}
                    disabled={isSubmitting}
                    className="py-2 px-3 border rounded-lg hover:bg-gray-50 text-sm capitalize disabled:opacity-50"
                  >
                    {stage === "final" ? "Final round" : stage}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Offer celebration */}
          {isOffer && (
            <>
              <div className="space-y-3">
                <label className="block text-sm font-medium text-gray-700">
                  What helped most? (select all that apply)
                </label>
                {[
                  "Tailored resume",
                  "Interview prep",
                  "Company research",
                  "Salary negotiation",
                  "Cultural fit",
                ].map((item) => (
                  <label key={item} className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={reflectionChecked[item] || false}
                      onChange={(e) =>
                        setReflectionChecked((prev) => ({
                          ...prev,
                          [item]: e.target.checked,
                        }))
                      }
                      className="rounded border-gray-300 text-brand-500 focus:ring-brand-500"
                    />
                    <span className="text-sm">{item}</span>
                  </label>
                ))}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Anything surprising? (optional)
                </label>
                <textarea
                  value={reflectionText}
                  onChange={(e) => setReflectionText(e.target.value)}
                  rows={2}
                  placeholder="Share what surprised you..."
                  className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                />
              </div>

              <button
                onClick={handleOfferCelebrate}
                disabled={isSubmitting}
                className="w-full py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
              >
                Celebrate! 🎉
              </button>
            </>
          )}

          {/* Other outcomes */}
          {!isOffer && (
            <details className="group">
              <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700 text-center py-2">
                Other outcomes ▾
              </summary>
              <div className="mt-2 space-y-2">
                <button
                  onClick={() => handleAdvanceStage("rejection")}
                  disabled={isSubmitting}
                  className="w-full py-2 border border-red-200 text-red-600 rounded-lg hover:bg-red-50 disabled:opacity-50"
                >
                  Not proceeding
                </button>
                <button
                  onClick={() => handleAdvanceStage("withdrawal")}
                  disabled={isSubmitting}
                  className="w-full py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  Withdrew application
                </button>
              </div>
            </details>
          )}
        </div>

        {/* Close */}
        <div className="px-4 pb-4">
          <button
            onClick={onClose}
            className="w-full py-2 text-gray-500 hover:text-gray-700 text-sm"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}
