import { useEffect, useState } from 'react'
import { Wrench, Clock, AlertTriangle, CheckCircle } from 'lucide-react'
import Layout from '../components/Layout'
import { maintenanceAPI } from '../api'

const priorityColors = {
  high: 'border-red-500/30 bg-red-500/5',
  medium: 'border-amber-500/30 bg-amber-500/5',
  low: 'border-green-500/30 bg-green-500/5',
}

export default function Maintenance() {
  const [records, setRecords] = useState([])
  const [summary, setSummary] = useState(null)

  useEffect(() => {
    Promise.all([maintenanceAPI.list(), maintenanceAPI.summary()])
      .then(([listRes, summaryRes]) => {
        setRecords(listRes.data)
        setSummary(summaryRes.data)
      })
      .catch(console.error)
  }, [])

  return (
    <Layout title="Maintenance Intelligence" subtitle="AI-powered predictive maintenance recommendations">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="stat-card">
          <p className="text-slate-400 text-sm">High Priority</p>
          <p className="text-4xl font-bold text-red-400 mt-1">{summary?.open_high_priority || 0}</p>
        </div>
        <div className="stat-card">
          <p className="text-slate-400 text-sm">Medium Priority</p>
          <p className="text-4xl font-bold text-amber-400 mt-1">{summary?.open_medium_priority || 0}</p>
        </div>
        <div className="stat-card">
          <p className="text-slate-400 text-sm">Low Priority</p>
          <p className="text-4xl font-bold text-green-400 mt-1">{summary?.open_low_priority || 0}</p>
        </div>
        <div className="stat-card">
          <p className="text-slate-400 text-sm">Est. Downtime</p>
          <p className="text-4xl font-bold text-white mt-1">{summary?.estimated_downtime_hours || 0}h</p>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Wrench className="w-5 h-5 text-blue-400" />
          Maintenance Recommendations
        </h3>
        <div className="space-y-4">
          {records.length === 0 ? (
            <p className="text-slate-400 text-sm text-center py-8">
              Upload maintenance documents to generate AI recommendations
            </p>
          ) : (
            records.map((rec) => (
              <div key={rec.id} className={`p-5 rounded-xl border ${priorityColors[rec.priority]}`}>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h4 className="font-semibold text-white">{rec.equipment}</h4>
                      <span className={`text-xs px-2 py-0.5 rounded-full capitalize font-medium ${
                        rec.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                        rec.priority === 'medium' ? 'bg-amber-500/20 text-amber-400' :
                        'bg-green-500/20 text-green-400'
                      }`}>
                        {rec.priority}
                      </span>
                    </div>
                    <p className="text-sm text-slate-300">{rec.recommendation}</p>
                    <div className="flex items-center gap-4 mt-3 text-xs text-slate-400">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {rec.estimated_downtime_hours}h downtime
                      </span>
                      <span>Confidence: {Math.round(rec.confidence * 100)}%</span>
                      <span className="capitalize">{rec.status}</span>
                    </div>
                  </div>
                  {rec.priority === 'high' ? (
                    <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0" />
                  ) : (
                    <CheckCircle className="w-5 h-5 text-slate-500 flex-shrink-0" />
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </Layout>
  )
}
