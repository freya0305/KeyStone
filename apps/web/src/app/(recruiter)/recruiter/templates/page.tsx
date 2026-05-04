"use client"

import { useState, useEffect, useCallback } from 'react'
import { apiRequest } from '@/lib/api'

interface Template {
  id: string
  name: string
  logo_s3_key: string | null
  brand_primary_color: string
  brand_secondary_color: string
  font_choice: string
  created_at: string
}

interface CreateTemplateRequest {
  name: string
  logo_s3_key?: string
  brand_primary_color: string
  brand_secondary_color: string
  font_choice: string
}

export default function TemplatesPage() {
  const [templates, setTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [newTemplate, setNewTemplate] = useState<CreateTemplateRequest>({
    name: '',
    brand_primary_color: '#4F46E5',
    brand_secondary_color: '#6B7280',
    font_choice: 'Inter',
  })

  const loadTemplates = useCallback(() => {
    apiRequest<Template[]>('/recruiter/templates')
      .then(setTemplates)
      .catch(() => setTemplates([]))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    loadTemplates()
  }, [loadTemplates])

  const handleCreate = async () => {
    if (!newTemplate.name.trim()) return
    setCreating(true)
    setError(null)
    try {
      await apiRequest<Template>('/recruiter/templates', {
        method: 'POST',
        body: newTemplate,
      })
      setShowCreate(false)
      setNewTemplate({
        name: '',
        brand_primary_color: '#4F46E5',
        brand_secondary_color: '#6B7280',
        font_choice: 'Inter',
      })
      loadTemplates()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create template')
    } finally {
      setCreating(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this template?')) return
    try {
      await apiRequest(`/recruiter/templates/${id}`, { method: 'DELETE' })
      setTemplates(prev => prev.filter(t => t.id !== id))
    } catch {
      setError('Failed to delete template')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">JD Templates</h1>
          <p className="text-gray-600">Reusable templates for consistent job descriptions.</p>
        </div>
        <button
          onClick={() => setShowCreate(true)}
          className="px-4 py-2 bg-purple-600 text-white text-sm rounded-lg hover:bg-purple-700"
        >
          + New Template
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
          {error}
        </div>
      )}

      {/* Create Modal */}
      {showCreate && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold mb-4">Create Template</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Template Name</label>
                <input
                  type="text"
                  value={newTemplate.name}
                  onChange={e => setNewTemplate(t => ({ ...t, name: e.target.value }))}
                  placeholder="e.g. Engineering - Singapore"
                  className="w-full px-3 py-2 border rounded-lg"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Primary Color</label>
                  <div className="flex gap-2">
                    <input
                      type="color"
                      value={newTemplate.brand_primary_color}
                      onChange={e => setNewTemplate(t => ({ ...t, brand_primary_color: e.target.value }))}
                      className="w-10 h-10 rounded border cursor-pointer"
                    />
                    <input
                      type="text"
                      value={newTemplate.brand_primary_color}
                      onChange={e => setNewTemplate(t => ({ ...t, brand_primary_color: e.target.value }))}
                      className="flex-1 px-3 py-2 border rounded-lg text-sm font-mono"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Secondary Color</label>
                  <div className="flex gap-2">
                    <input
                      type="color"
                      value={newTemplate.brand_secondary_color}
                      onChange={e => setNewTemplate(t => ({ ...t, brand_secondary_color: e.target.value }))}
                      className="w-10 h-10 rounded border cursor-pointer"
                    />
                    <input
                      type="text"
                      value={newTemplate.brand_secondary_color}
                      onChange={e => setNewTemplate(t => ({ ...t, brand_secondary_color: e.target.value }))}
                      className="flex-1 px-3 py-2 border rounded-lg text-sm font-mono"
                    />
                  </div>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Font</label>
                <select
                  value={newTemplate.font_choice}
                  onChange={e => setNewTemplate(t => ({ ...t, font_choice: e.target.value }))}
                  className="w-full px-3 py-2 border rounded-lg"
                >
                  <option value="Inter">Inter</option>
                  <option value="Roboto">Roboto</option>
                  <option value="Open Sans">Open Sans</option>
                  <option value="Lato">Lato</option>
                </select>
              </div>
            </div>
            <div className="flex gap-2 mt-6">
              <button
                onClick={() => setShowCreate(false)}
                className="flex-1 py-2 border rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleCreate}
                disabled={creating || !newTemplate.name.trim()}
                className="flex-1 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
              >
                {creating ? 'Creating...' : 'Create'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && <div className="text-center py-12 text-gray-500">Loading...</div>}

      {/* Templates Grid */}
      {!loading && templates.length > 0 && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map(template => (
            <div key={template.id} className="bg-white border rounded-xl p-5 hover:border-purple-300 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold text-gray-900">{template.name}</h3>
                <div className="flex gap-2">
                  <div
                    className="w-5 h-5 rounded border"
                    style={{ backgroundColor: template.brand_primary_color }}
                    title="Primary color"
                  />
                  <div
                    className="w-5 h-5 rounded border"
                    style={{ backgroundColor: template.brand_secondary_color }}
                    title="Secondary color"
                  />
                </div>
              </div>
              <div className="text-xs text-gray-500 mb-4">
                Font: {template.font_choice}
              </div>
              <div className="flex items-center justify-between pt-3 border-t">
                <span className="text-xs text-gray-500">
                  {new Date(template.created_at).toLocaleDateString('en-SG', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric',
                  })}
                </span>
                <div className="flex gap-1">
                  <Link
                    href={`/recruiter/jd?template=${template.id}`}
                    className="px-3 py-1.5 text-xs border rounded-lg hover:bg-gray-50"
                  >
                    Use
                  </Link>
                  <button
                    onClick={() => handleDelete(template.id)}
                    className="px-3 py-1.5 text-xs text-red-500 hover:text-red-700"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && templates.length === 0 && (
        <div className="bg-white border rounded-xl p-12 text-center">
          <div className="text-4xl mb-4">📋</div>
          <h3 className="font-semibold text-gray-900 mb-2">No templates yet</h3>
          <p className="text-gray-500 text-sm mb-6">
            Create your first template to speed up JD creation.
          </p>
          <button
            onClick={() => setShowCreate(true)}
            className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Create your first template
          </button>
        </div>
      )}
    </div>
  )
}
