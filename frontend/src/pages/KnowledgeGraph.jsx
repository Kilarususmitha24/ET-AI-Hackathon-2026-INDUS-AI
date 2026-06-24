import { useEffect, useState, useRef, useCallback } from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import { GitBranch, RefreshCw } from 'lucide-react'
import Layout from '../components/Layout'
import { graphAPI } from '../api'

const TYPE_COLORS = {
  Document: '#3b82f6',
  Equipment: '#10b981',
  Procedure: '#f59e0b',
  Regulation: '#ef4444',
  Incident: '#a855f7',
  Entity: '#64748b',
}

export default function KnowledgeGraph() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] })
  const [loading, setLoading] = useState(true)
  const graphRef = useRef()

  const loadGraph = useCallback(() => {
    setLoading(true)
    graphAPI.get()
      .then((res) => {
        const nodes = res.data.nodes.map((n) => ({
          id: n.id,
          name: n.label,
          type: n.type,
          val: n.type === 'Document' ? 8 : 5,
        }))
        const links = res.data.edges.map((e) => ({
          source: e.source,
          target: e.target,
          label: e.label,
        }))
        setGraphData({ nodes, links })
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => { loadGraph() }, [loadGraph])

  const nodeCount = graphData.nodes.length
  const edgeCount = graphData.links.length
  const types = [...new Set(graphData.nodes.map((n) => n.type))]

  return (
    <Layout title="Knowledge Graph" subtitle="Visualize relationships between equipment, procedures, incidents, and regulations">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="space-y-4">
          <div className="card p-5">
            <h3 className="text-sm font-semibold text-white mb-3">Graph Statistics</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-400">Nodes</span>
                <span className="text-white font-medium">{nodeCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Relationships</span>
                <span className="text-white font-medium">{edgeCount}</span>
              </div>
            </div>
            <button onClick={loadGraph} className="btn-secondary w-full mt-4 flex items-center justify-center gap-2 text-sm">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>

          <div className="card p-5">
            <h3 className="text-sm font-semibold text-white mb-3">Entity Types</h3>
            <div className="space-y-2">
              {types.map((type) => (
                <div key={type} className="flex items-center gap-2 text-sm">
                  <div className="w-3 h-3 rounded-full" style={{ background: TYPE_COLORS[type] || '#64748b' }} />
                  <span className="text-slate-300">{type}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:col-span-3 card overflow-hidden" style={{ height: 'calc(100vh - 200px)' }}>
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <GitBranch className="w-12 h-12 text-blue-400 animate-pulse" />
            </div>
          ) : nodeCount === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center p-8">
              <GitBranch className="w-16 h-16 text-slate-600 mb-4" />
              <p className="text-slate-400">Upload documents to build the knowledge graph</p>
            </div>
          ) : (
            <ForceGraph2D
              ref={graphRef}
              graphData={graphData}
              nodeLabel="name"
              nodeColor={(n) => TYPE_COLORS[n.type] || '#64748b'}
              linkLabel="label"
              linkColor={() => '#334155'}
              linkDirectionalArrowLength={4}
              linkDirectionalArrowRelPos={1}
              backgroundColor="#0f172a"
              nodeCanvasObject={(node, ctx, globalScale) => {
                const label = node.name
                const fontSize = 12 / globalScale
                ctx.beginPath()
                ctx.arc(node.x, node.y, node.val || 5, 0, 2 * Math.PI)
                ctx.fillStyle = TYPE_COLORS[node.type] || '#64748b'
                ctx.fill()
                ctx.font = `${fontSize}px Inter, sans-serif`
                ctx.textAlign = 'center'
                ctx.textBaseline = 'middle'
                ctx.fillStyle = '#e2e8f0'
                ctx.fillText(label?.substring(0, 20) || '', node.x, node.y + (node.val || 5) + fontSize)
              }}
            />
          )}
        </div>
      </div>
    </Layout>
  )
}
