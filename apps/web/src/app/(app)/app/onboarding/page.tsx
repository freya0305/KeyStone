"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useUser } from "@clerk/nextjs"
import { apiRequest } from "@/lib/api"
import { trackSignedUp } from "@/lib/analytics"
import { getOnboardingCompleteCopy, type Persona } from "@/lib/copy"

const PERSONA_OPTIONS = [
  { value: "fresh_grad", label: "Fresh grad, entering workforce" },
  { value: "switching", label: "Switching industry or function" },
  { value: "pmet", label: "Back on the market (PMET/retrenched)" },
  { value: "employed", label: "Currently employed, exploring options" },
]

const APPLICATION_COUNT_OPTIONS = [
  { value: "none", label: "None yet" },
  { value: "1-10", label: "1-10" },
  { value: "11-50", label: "11-50" },
  { value: "50+", label: "50+" },
]

interface OnboardingFormData {
  persona: string
  applicationCount: string
}

export default function OnboardingPage() {
  const router = useRouter()
  const { user } = useUser()
  const [step, setStep] = useState(0)
  const [formData, setFormData] = useState<OnboardingFormData>({
    persona: "",
    applicationCount: "",
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isComplete, setIsComplete] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handlePersonaSelect = (persona: string) => {
    setFormData((prev) => ({ ...prev, persona }))
    setStep(1)
  }

  const handleCountSelect = (count: string) => {
    setFormData((prev) => ({ ...prev, applicationCount: count }))
  }

  const handleSubmit = async () => {
    if (!formData.persona) {
      setError("Please select an option")
      return
    }

    setIsSubmitting(true)
    setError(null)

    try {
      // Determine persona string from selection
      const personaMap: Record<string, string> = {
        fresh_grad: "fresh_grad",
        switching: "switching",
        pmemt: "pmet",
        employed: "employed_exploring",
      }

      const storedPersona = personaMap[formData.persona] || formData.persona

      await apiRequest("/onboarding", {
        method: "POST",
        body: {
          looking_for: storedPersona,
          application_count: formData.applicationCount,
        },
      })

      // Track signed_up event
      // Determine method: check if user has any OAuth external accounts (Google, etc.)
      // In Clerk, externalAccounts tracks OAuth connections established during sign-in/sign-up
      const hasOAuthAccount =
        (user?.externalAccounts && user.externalAccounts.length > 0) ?? false
      trackSignedUp({ method: hasOAuthAccount ? "google" : "email" })

      // Store onboarding completed flag and persona
      localStorage.setItem("onboardingCompleted", "true")
      localStorage.setItem("onboardingPersona", storedPersona)

      // Show completion screen
      setIsComplete(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save onboarding data")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl w-full max-w-lg p-8">
        {step === 0 && (
          <>
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                What brings you to KeyStone today?
              </h1>
              <p className="text-gray-600">
                Help us personalize your experience
              </p>
            </div>

            <div className="space-y-3">
              {PERSONA_OPTIONS.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handlePersonaSelect(option.value)}
                  className="w-full p-4 text-left border rounded-lg hover:border-brand-500 hover:bg-brand-50 transition-colors"
                >
                  {option.label}
                </button>
              ))}
            </div>
          </>
        )}

        {step === 1 && (
          <>
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                How many jobs have you applied to recently?
              </h1>
              <p className="text-gray-600">
                This helps us calibrate expectations
              </p>
            </div>

            <div className="space-y-3">
              {APPLICATION_COUNT_OPTIONS.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleCountSelect(option.value)}
                  className={`w-full p-4 text-left border rounded-lg transition-colors ${
                    formData.applicationCount === option.value
                      ? "border-brand-500 bg-brand-50"
                      : "hover:border-brand-500 hover:bg-brand-50"
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>

            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                {error}
              </div>
            )}

            <div className="mt-6 flex gap-3">
              <button
                onClick={() => setStep(0)}
                className="flex-1 py-3 border rounded-lg hover:bg-gray-50"
              >
                Back
              </button>
              <button
                onClick={handleSubmit}
                disabled={isSubmitting || !formData.applicationCount}
                className="flex-1 py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50"
              >
                {isSubmitting ? "Saving..." : "Continue"}
              </button>
            </div>

            <p className="text-xs text-gray-500 text-center mt-4">
              You can always update these in Settings
            </p>
          </>
        )}

        {isComplete && (
          <>
            {(() => {
              const persona = (formData.persona === "fresh_grad" ? "fresh_grad" :
                formData.persona === "switching" ? "switching" :
                formData.persona === "pmet" ? "pmet" : "employed_exploring") as Persona
              const copy = getOnboardingCompleteCopy(persona)
              return (
                <div className="text-center py-4">
                  <h1 className="text-2xl font-bold text-gray-900 mb-2">
                    {copy.title}
                  </h1>
                  <p className="text-gray-600">
                    {copy.subtitle}
                  </p>
                </div>
              )
            })()}
            <div className="mt-6">
              <button
                onClick={() => router.push("/app")}
                className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600"
              >
                Go to Dashboard
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
