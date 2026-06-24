import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, FileText, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'
import Layout from '../components/Layout'
import { chatAPI } from '../api'

const SUGGESTIONS = [
  'What are the lockout/tagout procedures?',
  'Summarize pump P-101 maintenance requirements',
  'What OSHA compliance gaps exist?',
  'Describe the boiler safety inspection process',
]

export default function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const bottomRef = useRef()

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (text) => {
    if (!text.trim() || loading) return
    const userMsg = { role: 'user', content: text }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const res = await chatAPI.send(text, sessionId)
      if (!sessionId) setSessionId(res.data.session_id)
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: res.data.content,
        citations: res.data.citations || [],
      }])
    } catch (err) {
      toast.error('Failed to get response')
      setMessages((prev) => prev.slice(0, -1))
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout title="AI Knowledge Assistant" subtitle="RAG-powered industrial intelligence with source citations">
      <div className="card flex flex-col h-[calc(100vh-200px)]">
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <Bot className="w-16 h-16 text-blue-400 mx-auto mb-4 opacity-50" />
              <h3 className="text-xl font-semibold text-white mb-2">INDUS-AI Assistant</h3>
              <p className="text-slate-400 text-sm mb-6">Ask questions about your industrial knowledge base</p>
              <div className="flex flex-wrap gap-2 justify-center max-w-2xl mx-auto">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => sendMessage(s)}
                    className="text-xs px-3 py-2 bg-slate-800 border border-slate-600 rounded-full text-slate-300 hover:border-blue-500 hover:text-blue-400 transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-lg bg-blue-600/20 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-5 h-5 text-blue-400" />
                </div>
              )}
              <div className={`max-w-[75%] ${msg.role === 'user' ? 'order-first' : ''}`}>
                <div className={`rounded-2xl px-4 py-3 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-800 text-slate-100'
                }`}>
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                </div>
                {msg.citations?.length > 0 && (
                  <div className="mt-2 space-y-1">
                    <p className="text-xs text-slate-500 font-medium">Sources:</p>
                    {msg.citations.map((c, j) => (
                      <div key={j} className="text-xs p-2 bg-slate-800/50 rounded-lg border border-slate-700/50">
                        <div className="flex items-center gap-1 text-blue-400 mb-1">
                          <FileText className="w-3 h-3" />
                          {c.document_title}
                          {c.page && <span className="text-slate-500">p.{c.page}</span>}
                        </div>
                        <p className="text-slate-400 line-clamp-2">{c.chunk_text}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-lg bg-slate-700 flex items-center justify-center flex-shrink-0">
                  <User className="w-5 h-5 text-slate-300" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-lg bg-blue-600/20 flex items-center justify-center">
                <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
              </div>
              <div className="bg-slate-800 rounded-2xl px-4 py-3">
                <p className="text-sm text-slate-400">Analyzing knowledge base...</p>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="border-t border-slate-700/50 p-4">
          <form
            onSubmit={(e) => { e.preventDefault(); sendMessage(input) }}
            className="flex gap-3"
          >
            <input
              className="input-field flex-1"
              placeholder="Ask about maintenance, safety, compliance..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
            />
            <button type="submit" disabled={loading || !input.trim()} className="btn-primary px-5">
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>
      </div>
    </Layout>
  )
}
