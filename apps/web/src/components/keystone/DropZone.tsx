'use client';

import { useState, useCallback, useRef } from 'react';
import { apiRequest } from '@/lib/api';

type DropZoneState = 'idle' | 'dragging' | 'uploading' | 'success' | 'error';

interface DropZoneResult {
  state: DropZoneState;
  filename?: string;
  resumeId?: string;
  pageCount?: number;
  wordCount?: number;
  error?: string;
}

interface DropZoneProps {
  onFile?: (file: File, resumeId: string) => void;
  onText?: () => void;
  onUploadSuccess?: (result: DropZoneResult) => void;
  acceptedTypes?: string[];
  maxSizeMB?: number;
}

export function useDropZone({
  onFile,
  onUploadSuccess,
  acceptedTypes = ['.pdf', '.docx', '.doc', '.txt'],
  maxSizeMB = 10,
}: DropZoneProps) {
  const [result, setResult] = useState<DropZoneResult>({ state: 'idle' });
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): string | null => {
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!acceptedTypes.includes(ext)) {
      return 'Please upload a PDF, DOCX, or TXT file';
    }
    if (file.size > maxSizeMB * 1024 * 1024) {
      return `File must be smaller than ${maxSizeMB}MB`;
    }
    return null;
  };

  const uploadFile = useCallback(
    async (file: File) => {
      const error = validateFile(file);
      if (error) {
        setResult({ state: 'error', error });
        setTimeout(() => setResult({ state: 'idle' }), 3000);
        return;
      }

      setResult({ state: 'uploading', filename: file.name });

      try {
        // Get Clerk auth token
        const { getToken } = await import('@clerk/nextjs');
        const token = await getToken();
        const authHeaders: Record<string, string> = token
          ? { Authorization: `Bearer ${token}` }
          : {};

        const formData = new FormData();
        formData.append('file', file);

        const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const response = await fetch(`${API_BASE}/job-seeker/resume/upload`, {
          method: 'POST',
          headers: authHeaders,
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Upload failed');
        }

        const data = await response.json();
        const uploadResult: DropZoneResult = {
          state: 'success',
          filename: file.name,
          resumeId: data.id,
          pageCount: data.page_count,
          wordCount: data.word_count,
        };
        setResult(uploadResult);
        onFile?.(file, data.id);
        onUploadSuccess?.(uploadResult);
      } catch {
        setResult({ state: 'error', error: 'Failed to process file. Please try again.' });
        setTimeout(() => setResult({ state: 'idle' }), 3000);
      }
    },
    [onFile, onUploadSuccess, acceptedTypes, maxSizeMB]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setResult((r) => ({ ...r, state: 'dragging' }));
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setResult((r) => ({ ...r, state: 'idle' }));
  }, []);

  const handleDrop = useCallback(
    async (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();

      const file = e.dataTransfer.files[0];
      if (!file) {
        setResult({ state: 'idle' });
        return;
      }
      await uploadFile(file);
    },
    [uploadFile]
  );

  const handleFileInput = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (!file) return;
      await uploadFile(file);
    },
    [uploadFile]
  );

  const reset = useCallback(() => {
    setResult({ state: 'idle' });
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, []);

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
  };
}

export function DropZone({
  onFile,
  onText,
  onUploadSuccess,
}: Omit<DropZoneProps, 'onFile'> & { onFile?: (file: File, resumeId: string) => void }) {
  const { result, handlers, inputProps, reset } = useDropZone({ onFile, onText, onUploadSuccess });

  if (result.state === 'success' && result.filename) {
    return (
      <div className="border-2 border-match-strong/30 bg-match-strong-tint rounded-xl p-6 text-center">
        <div className="text-match-strong text-2xl mb-2">✓</div>
        <div className="font-medium text-stone-900 dark:text-stone-100">{result.filename}</div>
        {result.pageCount && result.wordCount && (
          <div className="text-sm text-stone-500 dark:text-stone-400 mt-1">
            {result.pageCount} page{result.pageCount !== 1 ? 's' : ''} · {result.wordCount} words
          </div>
        )}
        <button
          onClick={reset}
          className="mt-3 text-sm text-stone-500 dark:text-stone-400 hover:text-stone-700 dark:hover:text-stone-200 underline"
        >
          Upload a different file
        </button>
      </div>
    );
  }

  if (result.state === 'error') {
    return (
      <div className="border-2 border-red-300 bg-red-50 dark:bg-red-950/20 rounded-xl p-6 text-center">
        <div className="text-red-600 dark:text-red-400 text-sm">{result.error}</div>
        <button
          onClick={reset}
          className="mt-3 text-sm text-brand-600 dark:text-brand-400 hover:underline"
        >
          Try again
        </button>
        {onText && (
          <button
            onClick={onText}
            className="mt-2 block w-full text-sm text-stone-500 dark:text-stone-400 hover:text-stone-700 dark:hover:text-stone-200 underline"
          >
            Or paste text instead
          </button>
        )}
      </div>
    );
  }

  return (
    <div
      {...handlers}
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors cursor-pointer ${
        result.state === 'dragging'
          ? 'border-brand-400 bg-brand-50 dark:bg-brand-900/20'
          : 'border-stone-300 dark:border-stone-700 hover:border-brand-400 dark:hover:border-brand-500 hover:bg-stone-50 dark:hover:bg-brand-900/10'
      }`}
    >
      <div className="text-stone-400 dark:text-stone-500 text-3xl mb-3">📄</div>
      <p className="text-stone-700 dark:text-stone-200 font-medium mb-1">
        {result.state === 'uploading' ? 'Processing...' : 'Drop resume here'}
      </p>
      <p className="text-sm text-stone-500 dark:text-stone-400 mb-4">
        PDF, DOCX, or TXT — up to 10MB
      </p>
      <div className="flex items-center justify-center gap-3">
        <label className="px-4 py-2 bg-brand-500 text-white text-sm rounded-lg hover:bg-brand-600 cursor-pointer">
          Choose file
          <input {...inputProps} />
        </label>
        {onText && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onText();
            }}
            className="px-4 py-2 border border-stone-300 dark:border-stone-600 text-sm rounded-lg hover:bg-stone-50 dark:hover:bg-stone-800"
          >
            Or paste text
          </button>
        )}
      </div>
    </div>
  );
}
