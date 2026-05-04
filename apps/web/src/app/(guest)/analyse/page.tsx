"use client"

import { useState, useCallback } from "react"
import { DropZone } from "@/components/keystone/DropZone"
import { apiRequest } from "@/lib/api"

type AnalysisStep = "jd" | "resume" | "loading" | "results"
type Mode = "url" | "text"

interface JobParseResponse {
  job_id: string
  title: string | null
  company: string | null
  company_type: string | null
  skills: string[]
  seniority: string | null
  parsed_from: string
}

interface MatchAssessmentResponse {
  job_analysis_id: string
  match_levels: Record<string, "strong" | "transferable" | "addressable" | "fundamental">
  overall_score: number
  created_at: string
}

interface Suggestion {
  id: string
  section: string
  original_text: string
  suggested_text: string
  rationale: string | null
  match_level: string
  created_at: string
}

interface MatchResult {
  company: string
  role: string
  match_summary: {
    strong: number
    transferable: number
    addressable: number
    fundamental: number
  }
  suggestions: Suggestion[]
}

export default function AnalysePage() {
  const [step, setStep] = useState<AnalysisStep>("jd")
  const [mode, setMode] = useState<Mode>("url")
  const [jobUrl, setJobUrl] = useState("")
  const [jobText, setJobText] = useState("")
  const [resumeId, setResumeId] = useState<string | null>(null)
  const [jobId, setJobId] = useState<string | null>(null)
  const [loadingMessage, setLoadingMessage] = useState("")
  const [matchResult, setMatchResult] = useState<MatchResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  // Progress messages for loading screen
  const progressMessages = [
    { delay: 0, message: "Parsing job description..." },
    { delay: 2000, message: "Identifying key requirements..." },
    { delay: 4000, message: "Comparing with your experience..." },
    { delay: 6000, message: "Generating match suggestions..." },
  ]

  const handleJdNext = useCallback(() => {
    if (mode === "url" && !jobUrl.trim()) return
    if (mode === "text" && !jobText.trim()) return
    setStep("resume")
  }, [mode, jobUrl, jobText])

  const handleResumeUpload = useCallback(
    async (file: File, id: string) => {
      setResumeId(id)
      await startAnalysis(id)
    },
    []
  )

  const startAnalysis = async (rid: string) => {
    setStep("loading")
    setLoadingMessage(progressMessages[0].message)

    // Cycle through progress messages
    progressMessages.forEach(({ delay, message }) => {
      setTimeout(() => setLoadingMessage(message), delay)
    })

    try {
      // Step 1: Parse job description (URL or text)
      setLoadingMessage(progressMessages[0].message)
      const jdData = mode === "url" ? { url: jobUrl } : { text: jobText }
      const parseRes = await apiRequest<JobParseResponse>("/job-seeker/job/parse", {
        method: "POST",
        body: jdData,
      })

      setJobId(parseRes.job_id)

      // Step 2: Analyze match between resume and job
      setLoadingMessage(progressMessages[1].message)
      await apiRequest<MatchAssessmentResponse>(`/job-seeker/job/${parseRes.job_id}/analyze`, {
        method: "POST",
        body: { resume_id: rid },
      })

      // Step 3: Get suggestions
      setLoadingMessage(progressMessages[2].message)
      const suggestions = await apiRequest<Suggestion[]>("/job-seeker/suggestions", {
        method: "POST",
        body: { job_analysis_id: parseRes.job_id },
      })

      // Build match result from parse response and suggestions
      const matchLevels = suggestions.reduce(
        (acc, s) => {
          const level = s.match_level as keyof typeof acc
          if (level in acc) acc[level]++
          return acc
        },
        { strong: 0, transferable: 0, addressable: 0, fundamental: 0 } as Record<string, number>
      )

      setMatchResult({
        company: parseRes.company || "",
        role: parseRes.title || "",
        match_summary: matchLevels,
        suggestions,
      })

      setStep("results")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed")
      setStep("jd")
    }
  }

  const handleAccept = async (suggestionId: string) => {
    if (!jobId) return
    try {
      await apiRequest(`/job-seeker/suggestions/${suggestionId}/feedback`, {
        method: "POST",
        body: { action: "accept" },
      })
      // Update local state
      setMatchResult((prev) =>
        prev
          ? {
              ...prev,
              suggestions: prev.suggestions.map((s) =>
                s.id === suggestionId ? { ...s, accepted: true } : s
              ),
            }
          : null
      )
    } catch {
      // Silent failure - don't block user
    }
  }

  const handleReject = async (suggestionId: string) => {
    if (!jobId) return
    try {
      await apiRequest(`/job-seeker/suggestions/${suggestionId}/feedback`, {
        method: "POST",
        body: { action: "reject" },
      })
      setMatchResult((prev) =>
        prev
          ? {
              ...prev,
              suggestions: prev.suggestions.filter((s) => s.id !== suggestionId),
            }
          : null
      )
    } catch {
      // Silent failure
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-brand-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">KS</span>
            </div>
            <span className="font-semibold text-xl">KeyStone</span>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-3xl">
        {/* Step indicator */}
        <div className="flex items-center gap-2 mb-8">
          {["jd", "resume", "loading", "results"].map((s, i) => (
            <div key={s} className="flex items-center gap-2">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  step === s || ["resume", "loading", "results"].indexOf(step) > ["jd", "resume", "loading", "results"].indexOf(s)
                    ? "bg-brand-500 text-white"
                    : "bg-gray-200 text-gray-600"
                }`}
              >
                {i + 1}
              </div>
              {i < 3 && (
                <div className={`w-12 h-0.5 ${
                  ["resume", "loading", "results"].indexOf(step) > i ? "bg-brand-500" : "bg-gray-200"
                }`} />
              )}
            </div>
          ))}
        </div>

        {/* Error */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {/* Step 1: JD Input */}
        {step === "jd" && (
          <div className="bg-white border rounded-xl p-6 space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">
              What job are you targeting?
            </h1>

            {/* Mode toggle */}
            <div className="flex gap-4">
              <button
                type="button"
                onClick={() => { setMode("url"); setJobText("") }}
                className={`flex-1 p-4 border rounded-lg text-center transition-colors ${
                  mode === "url" ? "border-brand-500 bg-brand-50" : "hover:border-gray-300"
                }`}
              >
                <div className="text-2xl mb-2">🔗</div>
                <div className="font-medium">Job URL</div>
                <div className="text-sm text-gray-500">Paste from MyCareersFuture</div>
              </button>
              <button
                type="button"
                onClick={() => { setMode("text"); setJobUrl("") }}
                className={`flex-1 p-4 border rounded-lg text-center transition-colors ${
                  mode === "text" ? "border-brand-500 bg-brand-50" : "hover:border-gray-300"
                }`}
              >
                <div className="text-2xl mb-2">📋</div>
                <div className="font-medium">Paste Text</div>
                <div className="text-sm text-gray-500">Copy job description directly</div>
              </button>
            </div>

            {mode === "url" ? (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Job Posting URL
                </label>
                <input
                  type="url"
                  value={jobUrl}
                  onChange={(e) => setJobUrl(e.target.value)}
                  placeholder="https://..."
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                />
              </div>
            ) : (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Job Description
                </label>
                <textarea
                  value={jobText}
                  onChange={(e) => setJobText(e.target.value)}
                  rows={8}
                  placeholder="Paste job description here..."
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                />
              </div>
            )}

            <button
              type="button"
              onClick={handleJdNext}
              disabled={mode === "url" ? !jobUrl.trim() : !jobText.trim()}
              className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50"
            >
              Continue
            </button>
          </div>
        )}

        {/* Step 2: Resume Upload */}
        {step === "resume" && (
          <div className="bg-white border rounded-xl p-6 space-y-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Upload your resume
              </h1>
              <p className="text-gray-600 mt-1">
                We&apos;ll compare your experience with the job requirements.
              </p>
            </div>

            <DropZone
              onFile={handleResumeUpload}
              onText={() => {
                // For text paste, we'd need a different flow
                alert("Text paste for resume coming soon")
              }}
            />

            <button
              type="button"
              onClick={() => setStep("jd")}
              className="w-full py-2 border rounded-lg hover:bg-gray-50"
            >
              Back
            </button>
          </div>
        )}

        {/* Step 3: Loading */}
        {step === "loading" && (
          <div className="bg-white border rounded-xl p-12 text-center space-y-6">
            <div className="w-16 h-16 mx-auto border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                Analysing your match...
              </h2>
              <p className="text-gray-600">{loadingMessage}</p>
            </div>
            <div className="text-sm text-gray-500">
              This usually takes 10-30 seconds
            </div>
          </div>
        )}

        {/* Step 4: Results */}
        {step === "results" && matchResult && (
          <div className="space-y-6">
            {/* Match Summary */}
            <div className="bg-white border rounded-xl p-6">
              <h2 className="font-semibold text-lg mb-4">Match Summary</h2>
              <div className="grid grid-cols-4 gap-4">
                <div className="text-center p-4 bg-match-strong-tint rounded-lg">
                  <div className="text-3xl font-bold text-match-strong">
                    {matchResult.match_summary.strong}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Strong</div>
                </div>
                <div className="text-center p-4 bg-match-transferable-tint rounded-lg">
                  <div className="text-3xl font-bold text-match-transferable">
                    {matchResult.match_summary.transferable}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Transferable</div>
                </div>
                <div className="text-center p-4 bg-match-addressable-tint rounded-lg">
                  <div className="text-3xl font-bold text-match-addressable">
                    {matchResult.match_summary.addressable}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Addressable</div>
                </div>
                <div className="text-center p-4 bg-match-fundamental-tint rounded-lg">
                  <div className="text-3xl font-bold text-match-fundamental">
                    {matchResult.match_summary.fundamental}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Fundamental</div>
                </div>
              </div>
            </div>

            {/* Suggestions */}
            <div className="space-y-4">
              <h2 className="font-semibold text-lg">Suggestions</h2>
              {matchResult.suggestions
                .filter((s) => s.match_level !== "fundamental")
                .map((suggestion) => (
                  <SuggestionCard
                    key={suggestion.id}
                    suggestion={suggestion}
                    onAccept={() => handleAccept(suggestion.id)}
                    onReject={() => handleReject(suggestion.id)}
                  />
                ))}
            </div>

            {/* Fundamental gaps - collapsed by default */}
            {matchResult.match_summary.fundamental > 0 && (
              <details className="bg-white border rounded-xl">
                <summary className="p-4 cursor-pointer font-medium text-gray-700">
                  Worth knowing ({matchResult.match_summary.fundamental} gaps)
                </summary>
                <div className="px-4 pb-4 space-y-4">
                  {matchResult.suggestions
                    .filter((s) => s.match_level === "fundamental")
                    .map((suggestion) => (
                      <SuggestionCard
                        key={suggestion.id}
                        suggestion={suggestion}
                        onAccept={() => handleAccept(suggestion.id)}
                        onReject={() => handleReject(suggestion.id)}
                      />
                    ))}
                </div>
              </details>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

function SuggestionCard({
  suggestion,
  onAccept,
  onReject,
}: {
  suggestion: Suggestion
  onAccept: () => void
  onReject: () => void
}) {
  const [expanded, setExpanded] = useState(true)

  const levelColors: Record<string, string> = {
    strong: "bg-match-strong-tint text-match-strong border-match-strong",
    transferable: "bg-match-transferable-tint text-match-transferable border-match-transferable",
    addressable: "bg-match-addressable-tint text-match-addressable border-match-addressable",
    fundamental: "bg-match-fundamental-tint text-match-fundamental border-match-fundamental",
  }

  const levelClass = levelColors[suggestion.match_level] || levelColors.transferable

  return (
    <div className={`bg-white border rounded-xl overflow-hidden ${!expanded ? "opacity-60" : ""}`}>
      <div
        className="p-4 cursor-pointer flex items-start justify-between"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex-1">
          <span
            className={`inline-block px-2 py-0.5 text-xs font-medium rounded-full border ${levelClass}`}
          >
            {suggestion.match_level}
          </span>
          <p className="mt-2 text-sm text-gray-500">{suggestion.section}</p>
        </div>
        <div className="text-gray-400">{expanded ? "−" : "+"}</div>
      </div>

      {expanded && (
        <div className="px-4 pb-4 space-y-4">
          {/* Original */}
          <div>
            <div className="text-xs font-medium text-gray-500 mb-1">Original</div>
            <div className="p-3 bg-gray-50 rounded-lg font-mono text-sm">
              {suggestion.original_text}
            </div>
          </div>

          {/* Suggested */}
          <div>
            <div className="text-xs font-medium text-gray-500 mb-1">Suggested</div>
            <div className="p-3 bg-brand-50 border-l-2 border-brand-500 rounded-r-lg text-sm">
              {suggestion.suggested_text}
            </div>
          </div>

          {/* Rationale */}
          <div className="text-sm text-gray-600">{suggestion.rationale}</div>

          {/* Actions */}
          <div className="flex gap-2">
            <button
              onClick={onAccept}
              className="flex-1 py-2 bg-match-strong text-white text-sm rounded-lg hover:bg-match-strong/90"
            >
              ✓ Accept
            </button>
            <button
              onClick={onReject}
              className="flex-1 py-2 border text-sm rounded-lg hover:bg-gray-50"
            >
              ✗ Skip
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
