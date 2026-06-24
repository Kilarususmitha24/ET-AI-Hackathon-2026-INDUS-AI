import { useState } from 'react'
import { Search, AlertTriangle, Lightbulb, FileText, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'
import Layout from '../components/Layout'
import { rootCauseAPI } from '../api'

export default function RootCause() {
  const [form, setForm] = useState({
    equipment: '',
    incident_description: '',
    symptoms: '',
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!form.incident_description.trim()) {
      toast.error('Please describe the incident')
      return
    }
    setLoading(true)
    try {
      const res = await rootCauseAPI.analyze(form)
      setResult(res.data)
      toast.success('Root cause analysis complete')
    } catch {
      toast.error('Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout title="Root Cause Analysis" subtitle="AI-assisted incident investigation with knowledge base context">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Search className="w-5 h-5 text-blue-400" />
            Incident Details
          </h3>
          <form onSubmit={handleAnalyze} className="space-y-4">
            <div>
              <label className="text-sm text-slate-400 mb-1 block">Equipment</label>
              <input
                className="input-field"
                placeholder="e.g., Centrifugal Pump P-101"
                value={form.equipment}
                onChange={(e) => setForm({ ...form, equipment: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm text-slate-400 mb-1 block">Incident Description *</label>
              <textarea
                className="input-field min-h-[120px] resize-y"
                placeholder="Describe what happened..."
                value={form.incident_description}
                onChange={(e) => setForm({ ...form, incident_description: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="text-sm text-slate-400 mb-1 block">Symptoms & Observations</label>
              <textarea
                className="input-field min-h-[80px] resize-y"
                placeholder="Vibration, temperature, noise, alarms..."
                value={form.symptoms}
                onChange={(e) => setForm({ ...form, symptoms: e.target.value })}
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full flex items-center justify-center gap-2">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
              Analyze Root Cause
            </button>
          </form>
        </div>

        <div className="space-y-6">
          {!result ? (
            <div className="card p-12 text-center">
              <AlertTriangle className="w-16 h-16 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-400">Submit an incident to receive AI-powered root cause analysis</p>
            </div>
          ) : (
            <>
              <div className="card p-6">
                <h3 className="text-lg font-semibold text-white mb-3">Analysis Summary</h3>
                <p className="text-sm text-slate-300">{result.analysis_summary}</p>
              </div>

              <div className="card p-6">
                <h3 className="text-sm font-semibold text-red-400 mb-3 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4" />
                  Probable Causes
                </h3>
                <ul className="space-y-2">
                  {result.probable_causes.map((c, i) => (
                    <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                      <span className="text-red-400 font-bold">{i + 1}.</span> {c}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="card p-6">
                <h3 className="text-sm font-semibold text-amber-400 mb-3">Contributing Factors</h3>
                <ul className="space-y-2">
                  {result.contributing_factors.map((f, i) => (
                    <li key={i} className="text-sm text-slate-300">• {f}</li>
                  ))}
                </ul>
              </div>

              <div className="card p-6">
                <h3 className="text-sm font-semibold text-green-400 mb-3 flex items-center gap-2">
                  <Lightbulb className="w-4 h-4" />
                  Recommended Actions
                </h3>
                <ul className="space-y-2">
                  {result.recommended_actions.map((a, i) => (
                    <li key={i} className="text-sm text-slate-300">✓ {a}</li>
                  ))}
                </ul>
              </div>

              {result.related_documents?.length > 0 && (
                <div className="card p-6">
                  <h3 className="text-sm font-semibold text-blue-400 mb-3 flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    Related Documents
                  </h3>
                  {result.related_documents.map((doc, i) => (
                    <div key={i} className="text-xs p-3 bg-slate-800/50 rounded-lg mb-2">
                      <p className="text-blue-400 font-medium">{doc.document_title}</p>
                      <p className="text-slate-400 mt-1 line-clamp-2">{doc.chunk_text}</p>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </Layout>
  )
}
