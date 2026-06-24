import { useEffect, useState } from 'react'
import { FileText, MessageSquare, Shield, Wrench, GitBranch, AlertTriangle, TrendingUp } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import Layout from '../components/Layout'
import { analyticsAPI } from '../api'

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    analyticsAPI.dashboard()
      .then((res) => setStats(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <Layout title="Dashboard" subtitle="Loading analytics...">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="stat-card animate-pulse h-32" />
          ))}
        </div>
      </Layout>
    )
  }

  const statCards = [
    { label: 'Documents', value: stats?.total_documents || 0, sub: `${stats?.processed_documents || 0} processed`, icon: FileText, color: 'text-blue-400' },
    { label: 'Knowledge Chunks', value: stats?.total_chunks || 0, sub: 'Vector indexed', icon: GitBranch, color: 'text-purple-400' },
    { label: 'Compliance Score', value: `${stats?.compliance_score || 0}%`, sub: 'Regulatory readiness', icon: Shield, color: 'text-green-400' },
    { label: 'Open Maintenance', value: stats?.open_maintenance || 0, sub: 'Active recommendations', icon: Wrench, color: 'text-amber-400' },
  ]

  const chartData = [
    { name: 'Documents', value: stats?.total_documents || 0 },
    { name: 'Chunks', value: stats?.total_chunks || 0 },
    { name: 'KG Nodes', value: stats?.knowledge_graph_nodes || 0 },
    { name: 'Maintenance', value: stats?.open_maintenance || 0 },
  ]

  const pieData = [
    { name: 'Compliant', value: stats?.compliance_score || 0 },
    { name: 'Gap', value: 100 - (stats?.compliance_score || 0) },
  ]

  return (
    <Layout title="Operations Dashboard" subtitle="Real-time industrial knowledge intelligence overview">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map(({ label, value, sub, icon: Icon, color }) => (
          <div key={label} className="stat-card">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-slate-400 text-sm">{label}</p>
                <p className="text-3xl font-bold text-white mt-1">{value}</p>
                <p className="text-xs text-slate-500 mt-1">{sub}</p>
              </div>
              <div className={`p-3 rounded-xl bg-slate-800/80 ${color}`}>
                <Icon className="w-6 h-6" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-400" />
            Knowledge Base Metrics
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
              <YAxis stroke="#64748b" fontSize={12} />
              <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }} />
              <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-green-400" />
            Compliance Overview
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={90} dataKey="value" label>
                {pieData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          Recent Activity
        </h3>
        <div className="space-y-3">
          {(stats?.recent_activity || []).length === 0 ? (
            <p className="text-slate-400 text-sm">No recent activity. Upload documents to get started.</p>
          ) : (
            stats.recent_activity.map((item, i) => (
              <div key={i} className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <FileText className="w-4 h-4 text-blue-400" />
                  <span className="text-sm text-white">{item.title}</span>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full ${
                  item.status === 'processed' ? 'bg-green-500/20 text-green-400' :
                  item.status === 'processing' ? 'bg-amber-500/20 text-amber-400' :
                  'bg-slate-500/20 text-slate-400'
                }`}>
                  {item.status}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </Layout>
  )
}
