'use client';

import { useState, useCallback } from 'react';
import { apiRequest } from '@/lib/api';

interface Application {
  id: string;
  employer: string;
  role: string;
  status?: string;
}

interface InterviewPrepModalProps {
  isOpen: boolean;
  onClose: () => void;
  application: Application | null;
  /** "prep" = pre-interview (add notes), "outcome" = post-interview (record outcome) */
  mode: 'prep' | 'outcome';
  onSuccess?: () => void;
}

export function InterviewPrepModal({
  isOpen,
  onClose,
  application,
  mode,
  onSuccess,
}: InterviewPrepModalProps) {
  const [notes, setNotes] = useState('');
  const [outcome, setOutcome] = useState<string>('');
  const [nextRoundDate, setNextRoundDate] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = useCallback(async () => {
    if (!application) return;

    setIsSubmitting(true);
    try {
      if (mode === 'prep') {
        // Update application status to interview with prep notes
        await apiRequest(`/job-seeker/applications/${application.id}`, {
          method: 'PATCH',
          body: {
            status: 'interview',
            notes: notes.trim() || undefined,
          },
        });
      } else {
        // Record interview outcome
        await apiRequest(`/job-seeker/applications/${application.id}/stages`, {
          method: 'POST',
          body: {
            stage_type: 'interview',
            outcome: outcome || 'completed',
            notes: notes.trim() || undefined,
            stage_date: nextRoundDate || undefined,
          },
        });
      }
      onSuccess?.();
      onClose();
    } catch (err) {
      console.error('Failed to update interview:', err);
      alert('Failed to update. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  }, [application, mode, notes, outcome, nextRoundDate, onSuccess, onClose]);

  if (!isOpen || !application) return null;

  const isPrep = mode === 'prep';

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl w-full max-w-lg mx-4 overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-semibold">
                {application.employer} · {application.role}
              </h2>
              <p className="text-sm text-gray-500 mt-1">
                {isPrep ? 'Interview prep notes' : 'Record interview outcome'}
              </p>
            </div>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
              ✕
            </button>
          </div>
        </div>

        <div className="p-4 space-y-4">
          {isPrep ? (
            <>
              {/* Pre-interview: Prep notes */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Interview prep notes
                </label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  rows={4}
                  placeholder="Jot down what you want to prepare: company research, STAR stories, questions to ask..."
                  className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                />
                <p className="text-xs text-gray-500 mt-1">
                  These notes are saved with your application for future reference.
                </p>
              </div>
            </>
          ) : (
            <>
              {/* Post-interview: Outcome */}
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    How did it go?
                  </label>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      {
                        value: 'passed',
                        label: 'Passed',
                        color: 'bg-green-50 border-green-200 text-green-700 hover:bg-green-100',
                      },
                      {
                        value: 'pending',
                        label: 'Pending',
                        color: 'bg-yellow-50 border-yellow-200 text-yellow-700 hover:bg-yellow-100',
                      },
                      {
                        value: 'rejected',
                        label: 'Not for me',
                        color: 'bg-red-50 border-red-200 text-red-700 hover:bg-red-100',
                      },
                    ].map((opt) => (
                      <button
                        key={opt.value}
                        onClick={() => setOutcome(opt.value)}
                        className={`py-2 px-3 border rounded-lg text-sm font-medium transition-colors ${
                          outcome === opt.value
                            ? 'bg-brand-500 text-white border-brand-500'
                            : opt.color
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Notes (optional)
                  </label>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    rows={3}
                    placeholder="What went well? What would you do differently?"
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                  />
                </div>

                {outcome === 'passed' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Next round date (if known)
                    </label>
                    <input
                      type="date"
                      value={nextRoundDate}
                      onChange={(e) => setNextRoundDate(e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                    />
                  </div>
                )}
              </div>
            </>
          )}
        </div>

        {/* Actions */}
        <div className="px-4 pb-4 space-y-2">
          <button
            onClick={handleSubmit}
            disabled={isSubmitting || (!isPrep && !outcome)}
            className="w-full py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Saving...' : isPrep ? 'Start Interview Prep' : 'Record Outcome'}
          </button>
          <button
            onClick={onClose}
            className="w-full py-2 text-gray-500 hover:text-gray-700 text-sm"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
