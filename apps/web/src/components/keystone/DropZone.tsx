"use client"

import { useState, useCallback, useRef } from 'react'
import { apiRequest } from '@/lib/api'

type DropZoneState = 'idle' | 'dragging' | 'uploading' | 'success' | 'error'

interface DropZoneResult {
  state: DropZoneState
  filename?: string
  resumeId?: string
  pageCount?: number
  wordCount?: number
  error?: string
}

interface DropZoneProps {
  onFile?: (file: File, resumeId: string) => void
  onText?: () => void
  acceptedTypes?: string[]
  maxSizeMB?: number
}

export function useDropZone({
  onFile,
  acceptedTypes = ['.pdf', '.docx', '.doc', '.txt'],
  maxSizeMB = 10,
}: DropZoneProps) {
  const [result, setResult] = useState<DropZoneResult>({ state: 'idle' })
  const fileInputRef = useRef<HTMLInputElement>(null)

  const validateFile = (file: File): string | null => {
    const ext = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!acceptedTypes.includes(ext)) {
      return 'Please upload a PDF, DOCX, or TXT file'
    }
    if (file.size > maxSizeMB * 1024 * 1024) {
      return `File must be smaller than ${maxSizeMB}MB`
    }
    return null
  }

  const uploadFile = useCallback(async (file: File) => {
    const error = validateFile(file)
    if (error) {
      setResult({ state: 'error', error })
      setTimeout(() => setResult({ state: 'idle' }), 3000)
      return
    }

    setResult({ state: 'uploading', filename: file.name })

    try {
      // Get Clerk auth token
      let authHeaders: Record<string, string> = {}
      try {
        const { getToken } = await import('@clerk/nextjs/client')
        const token = await getToken()
        if (token) {
          authHeaders = { Authorization: `Bearer ${token}` }
        }
      } catch {
        // Not in Clerk context or not authenticated
      }

      const formData = new FormData()
      formData.append('file', file)

      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${API_BASE}/job-seeker/resume/upload`, {
        method: 'POST',
        headers: authHeaders,
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      const data = await response.json()
      setResult({
        state: 'success',
        filename: file.name,
        resumeId: data.id,
        pageCount: data.page_count,
        wordCount: data.word_count,
      })
      onFile?.(file, data.id)
    } catch {
      setResult({ state: 'error', error: 'Failed to process file. Please try again.' })
      setTimeout(() => setResult({ state: 'idle' }), 3000)
    }
  }, [onFile, acceptedTypes, maxSizeMB])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setResult(r => ({ ...r, state: 'dragging' }))
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setResult(r => ({ ...r, state: 'idle' }))
  }, [])

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()

    const file = e.dataTransfer.files[0]
    if (!file) {
      setResult({ state: 'idle' })
      return
    }
    await uploadFile(file)
  }, [uploadFile])

  const handleFileInput = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    await uploadFile(file)
  }, [uploadFile])

  const reset = useCallback(() => {
    setResult({ state: 'idle' })
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }, [])

  return {
    result,
    fileInputRef,
    handlers: {
      onDragOver: handleDragOver,
      onDragLeave: handleDragLeave,
      onDrop: handleDrop,
    },
    inputProps: {
      type: 'file' as const,
      accept: acceptedTypes.join(','),
      onChange: handleFileInput,
      ref: fileInputRef,
      className: 'hidden',
    },
    reset,
  }
}

export function DropZone({ onFile, onText }: Omit<DropZoneProps, 'onFile'> & { onFile?: (file: File, resumeId: string) => void }) {
  const { result, handlers, inputProps, reset } = useDropZone({ onFile, onText })

  if (result.state === 'success' && result.filename) {
    return (
      <div className="border-2 border-green-300 bg-green-50 rounded-xl p-6 text-center">
        <div className="text-green-600 text-2xl mb-2">✓</div>
        <div className="font-medium text-gray-900">{result.filename}</div>
        {result.pageCount && result.wordCount && (
          <div className="text-sm text-gray-500 mt-1">
            {result.pageCount} page{result.pageCount !== 1 ? 's' : ''} · {result.wordCount} words
          </div>
        )}
        <button
          onClick={reset}
          className="mt-3 text-sm text-gray-500 hover:text-gray-700 underline"
        >
          Upload a different file
        </button>
      </div>
    )
  }

  if (result.state === 'error') {
    return (
      <div className="border-2 border-red-300 bg-red-50 rounded-xl p-6 text-center">
        <div className="text-red-600 text-sm">{result.error}</div>
        <button
          onClick={reset}
          className="mt-3 text-sm text-blue-600 hover:underline"
        >
          Try again
        </button>
        {onText && (
          <button
            onClick={onText}
            className="mt-2 block w-full text-sm text-gray-500 hover:text-gray-700 underline"
          >
            Or paste text instead
          </button>
        )}
      </div>
    )
  }

  return (
    <div
      {...handlers}
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors cursor-pointer ${
        result.state === 'dragging'
          ? 'border-blue-400 bg-blue-50'
          : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
      }`}
    >
      <div className="text-gray-400 text-3xl mb-3">📄</div>
      <p className="text-gray-700 font-medium mb-1">
        {result.state === 'uploading' ? 'Processing...' : 'Drop resume here'}
      </p>
      <p className="text-sm text-gray-500 mb-4">
        PDF, DOCX, or TXT — up to 10MB
      </p>
      <div className="flex items-center justify-center gap-3">
        <label className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 cursor-pointer">
          Choose file
          <input {...inputProps} />
        </label>
        {onText && (
          <button
            onClick={(e) => {
              e.stopPropagation()
              onText()
            }}
            className="px-4 py-2 border text-sm rounded-lg hover:bg-gray-50"
          >
            Or paste text
          </button>
        )}
      </div>
    </div>
  )
}
