"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { DropZone } from "@/components/keystone/DropZone"
import { apiRequest } from "@/lib/api"

interface Resume {
  id: string
  filename: string
  uploaded_at: string
  page_count?: number
  word_count?: number
  analyses_count: number
}

export default function ResumesPage() {
  const [resumes, setResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)
  const [showUpload, setShowUpload] = useState(false)

  useEffect(() => {
    apiRequest<Resume[]>("/job-seeker/resumes")
      .then(setResumes)
      .catch(() => setResumes([]))
      .finally(() => setLoading(false))
  }, [])

  const handleUpload = async (file: File, resumeId: string) => {
    // Refresh the list
    try {
      const updated = await apiRequest<Resume[]>("/job-seeker/resumes")
      setResumes(updated)
    } catch {
      // Silent failure
    }
    setShowUpload(false)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Resumes</h1>
          <p className="text-gray-600">Manage your uploaded resumes</p>
        </div>
        <button
          onClick={() => setShowUpload(true)}
          className="px-4 py-2 bg-brand-500 text-white text-sm rounded-lg hover:bg-brand-600"
        >
          + Upload Resume
        </button>
      </div>

      {/* Upload Modal */}
      {showUpload && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold mb-4">Upload Resume</h2>
            <DropZone
              onFile={handleUpload}
              onText={() => {
                alert("Text paste for resume coming soon")
                setShowUpload(false)
              }}
            />
            <button
              onClick={() => setShowUpload(false)}
              className="mt-4 w-full py-2 border rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="text-center py-12 text-gray-500">Loading...</div>
      )}

      {/* Empty State */}
      {!loading && resumes.length === 0 && (
        <div className="bg-white border rounded-xl p-12 text-center">
          <div className="text-4xl mb-4">📄</div>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            No resumes yet
          </h2>
          <p className="text-gray-600 mb-6">
            Upload your first resume to get started with job analysis.
          </p>
          <button
            onClick={() => setShowUpload(true)}
            className="px-6 py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600"
          >
            Upload your first resume
          </button>
        </div>
      )}

      {/* Resume List */}
      {!loading && resumes.length > 0 && (
        <div className="bg-white border rounded-xl divide-y">
          {resumes.map((resume) => (
            <div
              key={resume.id}
              className="p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                    <span className="text-gray-500 text-xl">📄</span>
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">
                      {resume.filename}
                    </div>
                    <div className="text-sm text-gray-500">
                      {resume.page_count && resume.word_count
                        ? `${resume.page_count} pages · ${resume.word_count} words`
                        : "Uploaded"}{" "}
                      ·{" "}
                      {new Date(resume.uploaded_at).toLocaleDateString("en-SG", {
                        day: "numeric",
                        month: "short",
                        year: "numeric",
                      })}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-sm text-gray-500">
                    {resume.analyses_count} analysis{resume.analyses_count !== 1 ? "es" : ""}
                  </div>
                  <Link
                    href={`/app/resumes/${resume.id}`}
                    className="px-3 py-1.5 text-sm border rounded-lg hover:bg-gray-50"
                  >
                    View
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Privacy Note */}
      <div className="bg-gray-50 border rounded-xl p-4">
        <h3 className="font-medium text-gray-900 mb-1">Your privacy</h3>
        <p className="text-sm text-gray-600">
          Resumes are stored securely in Singapore. NRIC numbers are automatically detected and masked.
          You can delete your resume at any time from Settings.
        </p>
      </div>
    </div>
  )
}
