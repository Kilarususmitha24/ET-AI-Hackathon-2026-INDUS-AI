import { useEffect, useState } from 'react'
import { Shield, AlertTriangle, CheckCircle, AlertCircle } from 'lucide-react'
import Layout from '../components/Layout'
import { complianceAPI } from '../api'

const statusConfig = {
  compliant: { icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-500/10 border-green-500/30' },
  partial: { icon: AlertCircle, color: 'text-amber-400', bg: 'bg-amber-500/10 border-amber-500/30' },
  gap: { icon: AlertTriangle, color: 'text-red-400', bg: 'bg-red-500/10 border-red-500/30' },
}

export default function Compliance() {
  const [records, setRecords] = useState([])
  const [summary, setSummary] = useState(null)

  useEffect(() => {
    Promise.all([complianceAPI.list(), complianceAPI.summary()])
      .then(([listRes, summaryRes]) => {
        setRecords(listRes.data)
        setSummary(summaryRes.data)
      })
      .catch(console.error)
  }, [])

  return (
    <Layout title="Compliance Intelligence" subtitle="Automated regulatory gap detection and compliance monitoring">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="stat-card">
          <p className="text-slate-400 text-sm">Compliance Score</p>
          <p className="text-4xl font-bold text-green-400 mt-1">{summary?.compliance_score || 0}%</p>
        </div>
        <div className="stat-card">
          <p className="text-slate-400 text-sm">Compliant</p>
          <p className="text-4xl font-bold text-white mt-1">{summary?.compliant || 0}</p>
        </div>
        <div className="stat-card">
          <p className="text-slate-400 text-sm">Partial</p>
          <p className="text-4xl font-bold text-amber-400 mt-1">{summary?.partial || 0}</p>
        </div>
        <div className="stat-card">
          <p className="text-slate-400 text-sm">Gaps</p>
          <p className="text-4xl font-bold text-red-400 mt-1">{summary?.gaps || 0}</p>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Shield className="w-5 h-5 text-blue-400" />
          Regulatory Compliance Checks
        </h3>
        <div className="space-y-4">
          {records.length === 0 ? (
            <p className="text-slate-400 text-sm text-center py-8">
              Upload compliance-related documents to run automated checks
            </p>
          ) : (
            records.map((record) => {
              const config = statusConfig[record.status] || statusConfig.partial
              const Icon = config.icon
              return (
                <div key={record.id} className={`p-4 rounded-xl border ${config.bg}`}>
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <Icon className={`w-5 h-5 ${config.color}`} />
                        <span className="font-semibold text-white">{record.regulation}</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full capitalize ${config.color} bg-slate-800/50`}>
                          {record.status}
                        </span>
                      </div>
                      <p className="text-sm text-slate-300 mt-1">{record.requirement}</p>
                      {record.evidence && (
                        <p className="text-xs text-slate-400 mt-2">Evidence: {record.evidence}</p>
                      )}
                      {record.gap_description && (
                        <p className="text-xs text-red-400/80 mt-1">{record.gap_description}</p>
                      )}
                    </div>
                    <span className={`text-xs font-medium capitalize px-2 py-1 rounded ${
                      record.severity === 'high' ? 'bg-red-500/20 text-red-400' :
                      record.severity === 'medium' ? 'bg-amber-500/20 text-amber-400' :
                      'bg-green-500/20 text-green-400'
                    }`}>
                      {record.severity}
                    </span>
                  </div>
                </div>
              )
            })
          )}
        </div>
      </div>
    </Layout>
  )
}
