import { useRef, useState } from 'react'
import {
  Upload,
  FileText,
  Trash2,
  Loader2,
  CheckCircle2,
  AlertCircle,
  FileUp,
  Database,
  ScanText,
  X,
} from 'lucide-react'
import { uploadDocument, deleteDocument } from '../api'

const ALLOWED = ['.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg']
const MAX = 20 * 1024 * 1024

function formatSize(bytes) {
  if (!bytes) return '0 KB'

  const mb = bytes / (1024 * 1024)

  if (mb >= 1) {
    return `${mb.toFixed(1)} MB`
  }

  return `${Math.max(1, Math.round(bytes / 1024))} KB`
}

function getExtension(filename) {
  return '.' + filename.split('.').pop().toLowerCase()
}

function getFileIcon(filename) {
  const ext = getExtension(filename)

  if (['.png', '.jpg', '.jpeg'].includes(ext)) {
    return <ScanText size={18} />
  }

  return <FileText size={18} />
}

export default function DocumentPanel({ docs, onChanged }) {
  const inputRef = useRef(null)

  const [drag, setDrag] = useState(false)
  const [busy, setBusy] = useState(false)
  const [log, setLog] = useState([])

  const totals = docs?.totals || {
    documents: 0,
    pages: 0,
    chunks: 0,
  }

  const documents = docs?.documents || []

  async function handleFiles(fileList) {
    const files = Array.from(fileList || [])

    if (!files.length || busy) return

    setBusy(true)

    setLog(
      files.map((file) => ({
        name: file.name,
        size: file.size,
        state: 'waiting',
        msg: 'Waiting…',
      })),
    )

    const update = (index, patch) => {
      setLog((current) =>
        current.map((item, i) =>
          i === index
            ? { ...item, ...patch }
            : item,
        ),
      )
    }

    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      const ext = getExtension(file.name)

      if (!ALLOWED.includes(ext)) {
        update(i, {
          state: 'error',
          msg: 'File type not supported.',
        })
        continue
      }

      if (file.size > MAX) {
        update(i, {
          state: 'error',
          msg: 'File is larger than 20 MB.',
        })
        continue
      }

      update(i, {
        state: 'working',
        msg: 'Extracting and indexing…',
      })

      try {
        const response = await uploadDocument(file)

        update(i, {
          state: 'ok',
          msg:
            `Indexed · ${response.chunks} chunks` +
            (response.ocr_pages
              ? ` · OCR on ${response.ocr_pages} page(s)`
              : ''),
        })
      } catch (error) {
        update(i, {
          state: 'error',
          msg: error.message,
        })
      }
    }

    setBusy(false)

    if (inputRef.current) {
      inputRef.current.value = ''
    }

    await onChanged()
  }

  async function remove(document) {
    if (!window.confirm(`Delete ${document.filename}?`)) {
      return
    }

    try {
      await deleteDocument(document.doc_id)
      await onChanged()
    } catch (error) {
      alert(error.message)
    }
  }

  function clearLog() {
    if (!busy) {
      setLog([])
    }
  }

  return (
    <aside className="dp-panel">

      {/* HEADER */}
      <div className="dp-head">
        <h2>
          Documents
          <span className="dp-count">
            {totals.documents}
          </span>
        </h2>

        {totals.documents > 0 && (
          <span className="muted small">
            Knowledge base
          </span>
        )}
      </div>

      {/* UPLOAD AREA */}
      <div
        className={`dp-drop ${drag ? 'is-drag' : ''} ${
          busy ? 'is-busy' : ''
        }`}
        role="button"
        tabIndex={busy ? -1 : 0}
        onClick={() => {
          if (!busy) {
            inputRef.current?.click()
          }
        }}
        onKeyDown={(event) => {
          if (
            !busy &&
            (event.key === 'Enter' || event.key === ' ')
          ) {
            event.preventDefault()
            inputRef.current?.click()
          }
        }}
        onDragOver={(event) => {
          event.preventDefault()

          if (!busy) {
            setDrag(true)
          }
        }}
        onDragLeave={() => {
          setDrag(false)
        }}
        onDrop={(event) => {
          event.preventDefault()
          setDrag(false)

          if (!busy) {
            handleFiles(event.dataTransfer.files)
          }
        }}
      >

        <input
          ref={inputRef}
          type="file"
          multiple
          hidden
          accept=".pdf,.docx,.txt,.png,.jpg,.jpeg"
          onChange={(event) => {
            handleFiles(event.target.files)
          }}
        />

        {/* Animated document illustration */}
        <div className={`dp-art ${busy ? 'is-busy' : ''}`}>

          <svg
            viewBox="0 0 120 96"
            width="120"
            height="96"
            fill="none"
            aria-hidden="true"
          >
            <g className="dp-sheet dp-sheet-back">
              <rect
                x="18"
                y="15"
                width="62"
                height="66"
                rx="5"
                transform="rotate(-8 18 15)"
              />
            </g>

            <g className="dp-sheet dp-sheet-mid">
              <rect
                x="29"
                y="10"
                width="62"
                height="70"
                rx="5"
                transform="rotate(4 29 10)"
              />
            </g>

            <g className="dp-sheet dp-sheet-front">
              <path d="M43 10h31l18 18v53a5 5 0 0 1-5 5H43a5 5 0 0 1-5-5V15a5 5 0 0 1 5-5Z" />
              <path d="M74 10v18h18" />
            </g>

            <rect
              className="dp-line-strong"
              x="49"
              y="39"
              width="30"
              height="4"
              rx="2"
            />

            <rect
              className="dp-line"
              x="49"
              y="48"
              width="39"
              height="3"
              rx="1.5"
            />

            <rect
              className="dp-line"
              x="49"
              y="56"
              width="34"
              height="3"
              rx="1.5"
            />

            <rect
              className="dp-line"
              x="49"
              y="64"
              width="26"
              height="3"
              rx="1.5"
            />

            <rect
              className="dp-line-hot"
              x="49"
              y="72"
              width="17"
              height="3"
              rx="1.5"
            />
          </svg>

          <div className="dp-beam" />
        </div>

        <div className="dp-drop-title">
          {busy
            ? 'Processing documents…'
            : drag
              ? 'Drop files to upload'
              : 'Upload your documents'}
        </div>

        <div className="dp-drop-title">
          {!busy && !drag && (
            <span
              style={{
                fontSize: '0.78rem',
                fontWeight: 500,
                color: 'var(--text-dim)',
              }}
            >
              Drag & drop or click to browse
            </span>
          )}
        </div>

        <div className="dp-types">
          <span>PDF</span>
          <span>DOCX</span>
          <span>TXT</span>
          <span>PNG</span>
          <span>JPG</span>
        </div>

        <small>
          Maximum file size: 20 MB
        </small>
      </div>

      {/* UPLOAD LOG */}
      {log.length > 0 && (
        <div className="dp-log">

          <div className="dp-head">
            <h2 style={{ fontSize: '0.88rem' }}>
              Upload activity
              <span className="dp-count">
                {log.length}
              </span>
            </h2>

            {!busy && (
              <button
                className="dp-del"
                type="button"
                title="Clear upload activity"
                aria-label="Clear upload activity"
                onClick={clearLog}
              >
                <X size={14} />
              </button>
            )}
          </div>

          {log.map((item, index) => (
            <div
              key={`${item.name}-${index}`}
              className={`dp-log-row ${item.state}`}
            >

              <div>
                {item.state === 'working' && (
                  <Loader2
                    className="dp-spin"
                    size={16}
                  />
                )}

                {item.state === 'ok' && (
                  <CheckCircle2 size={16} />
                )}

                {item.state === 'error' && (
                  <AlertCircle size={16} />
                )}

                {item.state === 'waiting' && (
                  <FileText size={16} />
                )}
              </div>

              <div className="dp-log-text">
                <b title={item.name}>
                  {item.name}
                </b>

                <span>
                  {item.msg}
                </span>
              </div>

              <span
                style={{
                  marginLeft: 'auto',
                  flex: 'none',
                  fontSize: '0.68rem',
                  color: 'var(--text-dim)',
                }}
              >
                {formatSize(item.size)}
              </span>

              {item.state === 'working' && (
                <div className="dp-bar" />
              )}
            </div>
          ))}
        </div>
      )}

      {/* DOCUMENT LIBRARY */}
      <div>
        <div className="dp-head" style={{ marginBottom: '8px' }}>
          <h2 style={{ fontSize: '0.88rem' }}>
            Document library
          </h2>

          {documents.length > 0 && (
            <span className="muted small">
              {documents.length} loaded
            </span>
          )}
        </div>

        <div className="dp-list">

          {documents.length === 0 && (
            <div className="dp-empty">
              <FileText size={21} />

              <div>
                <b>No documents yet</b>

                <span>
                  Upload PDFs, Word files, text files or
                  images to start investigating.
                </span>
              </div>
            </div>
          )}

          {documents.map((document) => {
            const ext = getExtension(document.filename)

            return (
              <div
                className="dp-doc"
                key={document.doc_id}
              >

                <div
                  className={`dp-doc-icon ext-${ext.slice(1)}`}
                >
                  {getFileIcon(document.filename)}
                </div>

                <div className="dp-doc-main">

                  <div
                    className="dp-doc-name"
                    title={document.filename}
                  >
                    {document.filename}
                  </div>

                  <div className="dp-doc-meta">

                    <span>
                      {document.pages}{' '}
                      {document.pages === 1
                        ? 'page'
                        : 'pages'}
                    </span>

                    <span>·</span>

                    <span>
                      {document.chunks} chunks
                    </span>

                    {document.ocr_pages > 0 && (
                      <span className="dp-chip">
                        <ScanText size={10} />
                        OCR
                      </span>
                    )}
                  </div>

                </div>

                <button
                  className="dp-del"
                  type="button"
                  title={`Delete ${document.filename}`}
                  aria-label={`Delete ${document.filename}`}
                  disabled={busy}
                  onClick={() => remove(document)}
                >
                  <Trash2 size={15} />
                </button>

              </div>
            )
          })}
        </div>
      </div>

      {/* TOTALS */}
      {totals.documents > 0 && (
        <div className="dp-totals">

          <div>
            <b>{totals.documents}</b>
            <span>Documents</span>
          </div>

          <div>
            <b>{totals.pages}</b>
            <span>Pages</span>
          </div>

          <div>
            <b>{totals.chunks}</b>
            <span>Chunks</span>
          </div>

        </div>
      )}

    </aside>
  )
}