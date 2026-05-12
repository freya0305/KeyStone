'use client';

import { useState, useEffect, useCallback } from 'react';
import { apiRequest } from '@/lib/api';

interface JDGenerateRequest {
  title: string;
  company: string;
  industry: string;
  company_type?: 'banking' | 'fintech' | 'startup' | 'mnc' | 'other';
  skills: string[];
  seniority: 'junior' | 'mid' | 'senior' | 'lead';
}

interface JDGenerateResponse {
  id: string;
  title: string;
  company: string;
  content: string;
  word_count: number;
  generated_at: string;
}

interface SkillItem {
  skill: string;
  weighted_freq: number;
  required_count: number;
  preferred_count: number;
  total_jds: number;
}

interface SkillsLookupResponse {
  skills: SkillItem[];
  total_jds_analyzed: number;
  cold_start_warning?: string;
  prompt_for_manual_input: boolean;
  min_required_skills: number;
}

const SENIORITY_OPTIONS = [
  { value: 'junior', label: 'Junior (0-2 years)' },
  { value: 'mid', label: 'Mid-level (2-5 years)' },
  { value: 'senior', label: 'Senior (5-8 years)' },
  { value: 'lead', label: 'Lead / Manager (8+ years)' },
];

const COMPANY_TYPE_OPTIONS = [
  { value: 'banking', label: 'Banking & Finance' },
  { value: 'fintech', label: 'Fintech' },
  { value: 'startup', label: 'Startup' },
  { value: 'mnc', label: 'MNC / Large Corp' },
  { value: 'other', label: 'Other' },
];

const INDUSTRIES = [
  'Finance & Accounting',
  'Technology & Software',
  'Healthcare & Medical',
  'Engineering & Manufacturing',
  'Marketing & Communications',
  'Sales & Business Development',
  'Human Resources',
  'Operations & Logistics',
  'Legal & Compliance',
  'Education & Training',
  'Consulting',
  'Other',
];

export default function JDGeneratorPage() {
  const [form, setForm] = useState<JDGenerateRequest>({
    title: '',
    company: '',
    industry: '',
    company_type: undefined,
    skills: [],
    seniority: 'mid',
  });
  const [skillInput, setSkillInput] = useState('');
  const [result, setResult] = useState<JDGenerateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [skillSuggestions, setSkillSuggestions] = useState<SkillItem[]>([]);
  const [totalJdsAnalyzed, setTotalJdsAnalyzed] = useState<number | null>(null);
  const [skillsLoading, setSkillsLoading] = useState(false);

  // Map frontend industry free-text to DB slug (matches backend industry_map)
  const industrySlugMap: Record<string, string> = {
    'Finance & Accounting': 'banking_finance',
    'Technology & Software': 'technology',
    'Healthcare & Medical': 'healthcare',
    'Engineering & Manufacturing': 'engineering',
    'Marketing & Communications': 'other',
    'Sales & Business Development': 'other',
    'Human Resources': 'other',
    'Operations & Logistics': 'other',
    'Legal & Compliance': 'other',
    'Education & Training': 'education',
    Consulting: 'consulting',
    Other: 'other',
  };

  const fetchSkillSuggestions = useCallback(
    async (title: string, industry: string, seniority: string) => {
      if (!title || !industry) return;

      const industrySlug = industrySlugMap[industry] || 'other';
      setSkillsLoading(true);

      try {
        const params = new URLSearchParams({
          title,
          industry: industrySlug,
          seniority,
        });

        const response = await apiRequest<SkillsLookupResponse>(
          `/recruiter/skills/lookup?${params.toString()}`
        );
        setSkillSuggestions(response.skills);
        setTotalJdsAnalyzed(response.total_jds_analyzed);
      } catch (err) {
        // Silently fail - user can still manually enter skills
        console.error('Failed to fetch skill suggestions:', err);
        setSkillSuggestions([]);
        setTotalJdsAnalyzed(null);
      } finally {
        setSkillsLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    if (form.title && form.industry) {
      fetchSkillSuggestions(form.title, form.industry, form.seniority);
    }
  }, [form.title, form.industry, form.seniority, fetchSkillSuggestions]);

  const addSkill = (skill: string) => {
    const trimmed = skill.trim();
    if (trimmed && !form.skills.includes(trimmed) && form.skills.length < 20) {
      setForm((f) => ({ ...f, skills: [...f.skills, trimmed] }));
      setSkillInput('');
    }
  };

  const removeSkill = (skill: string) => {
    setForm((f) => ({ ...f, skills: f.skills.filter((s) => s !== skill) }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await apiRequest<JDGenerateResponse>('/recruiter/jd/generate', {
        method: 'POST',
        body: form,
      });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate JD');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Job Description Generator</h1>
        <p className="text-gray-600">Create professional JDs with AI in seconds.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6 bg-white border rounded-xl p-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Job Title *</label>
            <input
              type="text"
              required
              value={form.title}
              onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
              placeholder="e.g. Senior Software Engineer"
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Company Name *</label>
            <input
              type="text"
              required
              value={form.company}
              onChange={(e) => setForm((f) => ({ ...f, company: e.target.value }))}
              placeholder="e.g. DBS Bank"
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Industry *</label>
            <select
              required
              value={form.industry}
              onChange={(e) => setForm((f) => ({ ...f, industry: e.target.value }))}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            >
              <option value="">Select Industry</option>
              {INDUSTRIES.map((ind) => (
                <option key={ind} value={ind}>
                  {ind}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Company Type</label>
            <select
              value={form.company_type || ''}
              onChange={(e) =>
                setForm((f) => ({ ...f, company_type: (e.target.value as any) || undefined }))
              }
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            >
              <option value="">Select type...</option>
              {COMPANY_TYPE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Seniority *</label>
            <select
              required
              value={form.seniority}
              onChange={(e) => setForm((f) => ({ ...f, seniority: e.target.value as any }))}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            >
              {SENIORITY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Required Skills * (1-20)
            </label>
            <div className="flex gap-2 mb-2 flex-wrap">
              {form.skills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-700 rounded text-sm"
                >
                  {skill}
                  <button
                    type="button"
                    onClick={() => removeSkill(skill)}
                    className="hover:text-purple-900"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
            <div className="flex gap-2">
              <input
                type="text"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    addSkill(skillInput);
                  }
                }}
                placeholder="Type a skill and press Enter"
                className="flex-1 px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              />
              <button
                type="button"
                onClick={() => addSkill(skillInput)}
                className="px-3 py-2 border rounded-lg hover:bg-gray-50"
              >
                Add
              </button>
            </div>
            <div className="mt-2 flex flex-wrap gap-1">
              {skillsLoading ? (
                <span className="text-xs text-gray-400 px-2 py-1">Loading suggestions...</span>
              ) : skillSuggestions.length > 0 ? (
                skillSuggestions
                  .filter((s) => !form.skills.includes(s.skill))
                  .slice(0, 8)
                  .map((item) => (
                    <button
                      key={item.skill}
                      type="button"
                      onClick={() => addSkill(item.skill)}
                      className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded hover:bg-gray-200"
                      title={`Found in ${item.total_jds} JDs`}
                    >
                      + {item.skill}
                    </button>
                  ))
              ) : (
                <span className="text-xs text-gray-400 px-2 py-1">No suggestions available</span>
              )}
            </div>
            {totalJdsAnalyzed !== null && totalJdsAnalyzed > 0 && (
              <p className="mt-1 text-xs text-gray-500">
                Based on {totalJdsAnalyzed} job descriptions analyzed
              </p>
            )}
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={
              loading || !form.title || !form.company || !form.industry || form.skills.length === 0
            }
            className="w-full py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Generating...' : 'Generate Job Description'}
          </button>
        </form>

        {/* Result */}
        <div className="space-y-4">
          {result ? (
            <div className="bg-white border rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-lg">{result.title}</h2>
                <span className="text-sm text-gray-500">{result.word_count} words</span>
              </div>
              <div className="text-sm text-gray-500 mb-2">{result.company}</div>
              <div className="prose prose-sm max-w-none">
                <pre className="whitespace-pre-wrap text-sm text-gray-700 font-sans bg-gray-50 p-4 rounded-lg">
                  {result.content}
                </pre>
              </div>
              <div className="mt-4 flex gap-2">
                <button className="px-4 py-2 bg-purple-600 text-white text-sm rounded-lg hover:bg-purple-700">
                  Copy
                </button>
                <button className="px-4 py-2 border text-sm rounded-lg hover:bg-gray-50">
                  Save Version
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white border rounded-xl p-6 h-full flex items-center justify-center text-gray-400">
              <div className="text-center">
                <div className="text-4xl mb-2">📝</div>
                <p>Generated job description will appear here</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
