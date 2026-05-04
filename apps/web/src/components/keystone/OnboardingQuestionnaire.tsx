"use client"

import { useState } from "react"
import { apiRequest } from "@/lib/api"

interface OnboardingQuestionnaireProps {
  onComplete: (persona: string) => void
}

const LOOKING_FOR_OPTIONS = [
  { value: "fresh_grad", label: "Fresh grad, entering workforce" },
  { value: "switching", label: "Switching industry or function" },
  { value: "pmet", label: "Back on the market (PMET/retrenched)" },
  { value: "employed", label: "Currently employed, exploring options" },
]

const APPLICATION_COUNT_OPTIONS = [
  { value: "0", label: "None yet" },
  { value: "1-10", label: "1-10" },
  { value: "11-50", label: "11-50" },
  { value: "50+", label: "50+" },
]

export function OnboardingQuestionnaire({
  onComplete,
}: OnboardingQuestionnaireProps) {
  const [step, setStep] = useState(0)
  const [lookingFor, setLookingFor] = useState("")
  const [appCount, setAppCount] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async () => {
    setIsSubmitting(true)
    try {
      await apiRequest("/job-seeker/onboarding", {
        method: "POST",
        body: {
          looking_for: lookingFor,
          application_count: appCount,
        },
      })
      onComplete(lookingFor)
    } catch {
      // Still complete locally even if API fails
      onComplete(lookingFor)
    } finally {
      setIsSubmitting(false)
    }
  }

  const canProceed = step === 0 ? lookingFor : appCount

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl w-full max-w-md mx-4 overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b text-center">
          <h2 className="text-xl font-bold text-gray-900">
            Welcome to KeyStone
          </h2>
          <p className="text-gray-500 text-sm mt-1">
            Help us personalize your experience
          </p>
        </div>

        {/* Progress */}
        <div className="px-6 pt-4">
          <div className="flex gap-1">
            {[0, 1].map((i) => (
              <div
                key={i}
                className={`h-1 flex-1 rounded-full ${
                  i <= step ? "bg-brand-500" : "bg-gray-200"
                }`}
              />
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {step === 0 && (
            <div className="space-y-3">
              <h3 className="font-medium text-gray-900">
                What brings you to KeyStone today?
              </h3>
              <div className="space-y-2">
                {LOOKING_FOR_OPTIONS.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => setLookingFor(option.value)}
                    className={`w-full p-3 text-left rounded-lg border transition-colors ${
                      lookingFor === option.value
                        ? "border-brand-500 bg-brand-50"
                        : "hover:bg-gray-50"
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {step === 1 && (
            <div className="space-y-3">
              <h3 className="font-medium text-gray-900">
                How many jobs have you applied to recently?
              </h3>
              <div className="grid grid-cols-2 gap-2">
                {APPLICATION_COUNT_OPTIONS.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => setAppCount(option.value)}
                    className={`p-3 rounded-lg border transition-colors ${
                      appCount === option.value
                        ? "border-brand-500 bg-brand-50"
                        : "hover:bg-gray-50"
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t flex gap-2">
          {step > 0 && (
            <button
              onClick={() => setStep((s) => s - 1)}
              className="flex-1 py-2 border rounded-lg hover:bg-gray-50"
            >
              Back
            </button>
          )}
          <button
            onClick={step === 0 ? () => setStep(1) : handleSubmit}
            disabled={!canProceed || isSubmitting}
            className="flex-1 py-2 bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50"
          >
            {isSubmitting ? "Saving..." : step === 0 ? "Continue" : "Get started"}
          </button>
        </div>
      </div>
    </div>
  )
}
