import { useEffect, useState, useRef } from 'react'
import { Upload, FileText, Trash2, Loader2, CheckCircle, Clock, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'
import Layout from '../components/Layout'
import { documentsAPI } from '../api'

const CATEGORIES = ['general', 'maintenance', 'safety', 'compliance', 'incident', 'procedure']

const statusIcon = {
  processed: <CheckCircle className="w-4 h-4 text-green-400" />,
  processing: <Loader2 className="w-4 h-4 text-amber-400 animate-spin" />,
  pending: <Clock className="w-4 h-4 text-slate-400" />,
  failed: <AlertCircle className="w-4 h-4 text-red-400" />,
}

export default function Documents() {
  const [documents, setDocuments] = useState([])
  const [uploading, setUploading] = useState(false)
  const [category, setCategory] = useState('general')
  const fileRef = useRef()

  const loadDocs = () => {
    documentsAPI.list().then((res) => setDocuments(res.data)).catch(console.error)
  }

  useEffect(() => {
    loadDocs()
    const interval = setInterval(loadDocs, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleUpload = async (e) => {
    const files = e.target.files
    if (!files?.length) return
    setUploading(true)
    try {
      for (const file of files) {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('title', file.name)
        formData.append('doc_category', category)
        await documentsAPI.upload(formData)
      }
      toast.success(`${files.length} document(s) uploaded for processing`)
      loadDocs()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
      if (fileRef.current) fileRef.current.value = ''
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this document?')) return
    try {
      await documentsAPI.delete(id)
      toast.success('Document deleted')
      loadDocs()
    } catch {
      toast.error('Delete failed')
    }
  }

  return (
    <Layout title="Document Management" subtitle="Upload and manage industrial knowledge documents">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Upload Documents</h3>
          <div className="space-y-4">
            <div>
              <label className="text-sm text-slate-400 mb-1 block">Category</label>
              <select
                className="input-field"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
                ))}
              </select>
            </div>
            <div
              className="border-2 border-dashed border-slate-600 rounded-xl p-8 text-center hover:border-blue-500/50 transition-colors cursor-pointer"
              onClick={() => fileRef.current?.click()}
            >
              <Upload className="w-10 h-10 text-blue-400 mx-auto mb-3" />
              <p className="text-white font-medium">Drop files or click to upload</p>
              <p className="text-xs text-slate-400 mt-2">PDF, DOCX, PNG, JPG, TIFF</p>
              <input
                ref={fileRef}
                type="file"
                multiple
                accept=".pdf,.docx,.png,.jpg,.jpeg,.tiff,.txt"
                className="hidden"
                onChange={handleUpload}
              />
            </div>
            {uploading && (
              <div className="flex items-center gap-2 text-blue-400 text-sm">
                <Loader2 className="w-4 h-4 animate-spin" />
                Processing upload...
              </div>
            )}
          </div>
        </div>

        <div className="lg:col-span-2 card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Documents ({documents.length})
          </h3>
          <div className="space-y-3 max-h-[600px] overflow-y-auto">
            {documents.length === 0 ? (
              <p className="text-slate-400 text-sm text-center py-12">
                No documents yet. Upload sample industrial documents to begin.
              </p>
            ) : (
              documents.map((doc) => (
                <div key={doc.id} className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg hover:bg-slate-800 transition-colors">
                  <div className="flex items-center gap-4 min-w-0">
                    <div className="p-2 bg-blue-500/10 rounded-lg">
                      <FileText className="w-5 h-5 text-blue-400" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-white font-medium truncate">{doc.title}</p>
                      <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
                        <span className="capitalize">{doc.doc_category}</span>
                        <span>{doc.page_count} pages</span>
                        <span>{doc.chunk_count} chunks</span>
                        {doc.ocr_applied && <span className="text-purple-400">OCR</span>}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-1">
                      {statusIcon[doc.status]}
                      <span className="text-xs text-slate-400 capitalize">{doc.status}</span>
                    </div>
                    <button
                      onClick={() => handleDelete(doc.id)}
                      className="p-2 text-slate-400 hover:text-red-400 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </Layout>
  )
}
