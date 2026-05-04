"use client"

import { useState, useEffect } from "react"

interface StageProgressionProps {
  isOpen: boolean
  onClose: () => void
  application: {
    company: string
    role: string
    previousStage: string
    newStage: string
    isOffer?: boolean
  }
  onSave: (data: { nextRoundFormat?: string; nextRoundDate?: string }) => void
}

const STAGE_OPTIONS = [
  "Phone screening",
  "Round 1",
  "Round 2",
  "Final round",
  "Reference check",
  "Offer",
]

const ROUND_FORMATS = [
  "Phone",
  "Video",
  "In-person",
  "Panel",
  "Technical",
  "Case study",
]

export function StageProgressionModal({
  isOpen,
  onClose,
  application,
  onSave,
}: StageProgressionProps) {
  const [selectedFormat, setSelectedFormat] = useState<string>("")
  const [selectedDate, setSelectedDate] = useState<string>("")
  const [showConfetti, setShowConfetti] = useState(false)

  useEffect(() => {
    if (isOpen && application.isOffer) {
      setShowConfetti(true)
      const timer = setTimeout(() => setShowConfetti(false), 2400)
      return () => clearTimeout(timer)
    } else if (isOpen) {
      setShowConfetti(true)
      const timer = setTimeout(() => setShowConfetti(false), 1200)
      return () => clearTimeout(timer)
    }
  }, [isOpen, application.isOffer])

  if (!isOpen) return null

  const handleSave = () => {
    onSave({
      nextRoundFormat: selectedFormat || undefined,
      nextRoundDate: selectedDate || undefined,
    })
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      {/* Confetti */}
      {showConfetti && (
        <div className="fixed inset-0 pointer-events-none overflow-hidden">
          {Array.from({ length: 12 }).map((_, i) => (
            <div
              key={i}
              className="confetti-piece"
              style={{
                left: `${10 + (i * 7)}%`,
                animationDelay: `${i * 0.1}s`,
                backgroundColor: ["#1E7A8C", "#1F8F5F", "#C68A1A", "#D97338"][
                  i % 4
                ],
              }}
            />
          ))}
        </div>
      )}

      <div className="bg-white rounded-xl w-full max-w-md mx-4 overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b">
          <h2 className="font-semibold text-lg">
            {application.company} · {application.role}
          </h2>
        </div>

        {/* Content */}
        <div className="p-4 space-y-4">
          <div>
            <h3 className="font-medium mb-2">What just happened?</h3>
            <div className="space-y-2">
              {application.previousStage !== application.newStage && (
                <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg cursor-pointer">
                  <input
                    type="radio"
                    name="stage"
                    checked={application.newStage === "Offer"}
                    readOnly
                  />
                  <span>
                    {application.previousStage} — advancing to {application.newStage}
                  </span>
                </label>
              )}
              {application.isOffer && (
                <label className="flex items-center gap-3 p-3 bg-match-strong-tint rounded-lg">
                  <span className="text-2xl">🎉</span>
                  <span className="font-medium">Got an offer!</span>
                </label>
              )}
            </div>
          </div>

          {/* Next round info */}
          {!application.isOffer && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Format of next round
                </label>
                <div className="flex flex-wrap gap-2">
                  {ROUND_FORMATS.map((format) => (
                    <button
                      key={format}
                      onClick={() => setSelectedFormat(format)}
                      className={`px-3 py-1.5 text-sm rounded-lg border ${
                        selectedFormat === format
                          ? "bg-brand-50 border-brand-500 text-brand-700"
                          : "hover:bg-gray-50"
                      }`}
                    >
                      {format}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date of next round
                </label>
                <input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg"
                />
              </div>
            </>
          )}

          {/* Offer reflection */}
          {application.isOffer && (
            <div className="bg-match-strong-tint rounded-lg p-4">
              <p className="text-sm text-gray-700">
                Congratulations! This is the highest-value data point for
                improving KeyStone&apos;s recommendations.
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t flex gap-2">
          <button
            onClick={onClose}
            className="flex-1 py-2 border rounded-lg hover:bg-gray-50"
          >
            Maybe later
          </button>
          <button
            onClick={handleSave}
            className="flex-1 py-2 bg-brand-500 text-white rounded-lg hover:bg-brand-600"
          >
            {application.isOffer ? "Save" : "Save advancement"}
          </button>
        </div>
      </div>

      <style jsx>{`
        .confetti-piece {
          position: absolute;
          width: 10px;
          height: 10px;
          top: -20px;
          border-radius: 2px;
          animation: fall 1.2s ease-in forwards;
        }
        @keyframes fall {
          0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
          }
          100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  )
}
