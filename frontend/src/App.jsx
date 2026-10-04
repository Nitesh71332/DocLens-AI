import { useCallback, useEffect, useState } from 'react'
import { health, listDocuments } from './api'
import DocumentPanel from './components/DocumentPanel'
import Investigation from './components/Investigation'
import EvidencePanel from './components/EvidencePanel'
import ConflictCenter from './components/ConflictCenter'

const EMPTY = {
  documents: [],
  totals: {
    documents: 0,
    pages: 0,
    chunks: 0,
  },
}

function BrandIcon() {
  return (
    <div className="brand-icon">
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
        <polyline points="14 2 14 8 20 8" />
        <circle cx="11" cy="14" r="3" />
        <line x1="13.1" y1="16.1" x2="16" y2="19" />
      </svg>
    </div>
  )
}

function SearchIcon() {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  )
}

function ConflictIcon() {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
      <line x1="12" y1="9" x2="12" y2="13" />
      <line x1="12" y1="17" x2="12.01" y2="17" />
    </svg>
  )
}

export default function App() {
  const [tab, setTab] = useState('investigate')
  const [docs, setDocs] = useState(EMPTY)
  const [online, setOnline] = useState(null)
  const [result, setResult] = useState(null)
  const [version, setVersion] = useState(0)
  const [autoAsk, setAutoAsk] = useState(null)

  const refreshDocs = useCallback(async () => {
    try {
      const data = await listDocuments()
      setDocs(data || EMPTY)
      setOnline(true)
    } catch {
      setOnline(false)
    }
  }, [])

  useEffect(() => {
    refreshDocs()

    health()
      .then(() => setOnline(true))
      .catch(() => setOnline(false))
  }, [refreshDocs])

  async function onChanged() {
    setResult(null)
    setVersion((v) => v + 1)
    await refreshDocs()
  }

  function investigateTopic(topic) {
    setAutoAsk({
      q: `What is the ${topic}?`,
    })
    setTab('investigate')
  }

  const hasDocs = docs.totals?.documents > 0

  return (
    <div className="app">
      <header className="header">

        <div className="brand">
          <BrandIcon />

          <div>
            <div>DocuLens AI</div>
            <small>Evidence-first document investigator</small>
          </div>
        </div>

        <div
          className="muted small"
          style={{
            display: 'flex',
            gap: '18px',
            marginLeft: '10px',
            paddingLeft: '22px',
            borderLeft: '1px solid var(--line)',
          }}
        >
          <div>
            <strong style={{ color: 'var(--text)', fontSize: '15px' }}>
              {docs.totals?.documents || 0}
            </strong>
            <span style={{ marginLeft: '5px' }}>Docs</span>
          </div>

          <div>
            <strong style={{ color: 'var(--text)', fontSize: '15px' }}>
              {docs.totals?.pages || 0}
            </strong>
            <span style={{ marginLeft: '5px' }}>Pages</span>
          </div>

          <div>
            <strong style={{ color: 'var(--text)', fontSize: '15px' }}>
              {docs.totals?.chunks || 0}
            </strong>
            <span style={{ marginLeft: '5px' }}>Chunks</span>
          </div>
        </div>

        <nav className="tabs">

          <button
            className={`tab ${tab === 'investigate' ? 'active' : ''}`}
            onClick={() => setTab('investigate')}
          >
            <SearchIcon />
            <span>Investigate</span>
          </button>

          <button
            className={`tab ${tab === 'conflicts' ? 'active' : ''}`}
            onClick={() => setTab('conflicts')}
          >
            <ConflictIcon />
            <span>Conflict Center</span>
          </button>

        </nav>

        <div className="status">
          <span
            className={`dot ${
              online === null ? '' : online ? 'on' : 'off'
            }`}
          />

          <span>
            {online === null
              ? 'Connecting…'
              : online
                ? 'Backend Connected'
                : 'Backend Offline'}
          </span>
        </div>

      </header>

      <div
        className={`layout ${
          tab === 'investigate' ? 'three' : 'two'
        }`}
      >

        <DocumentPanel
          docs={docs}
          onChanged={onChanged}
        />

        {tab === 'investigate' ? (
          <>
            <Investigation
              hasDocs={hasDocs}
              result={result}
              setResult={setResult}
              autoAsk={autoAsk}
              clearAutoAsk={() => setAutoAsk(null)}
            />

            <EvidencePanel
              result={result}
            />
          </>
        ) : (
          <ConflictCenter
            version={version}
            hasDocs={hasDocs}
            onInvestigate={investigateTopic}
          />
        )}

      </div>
    </div>
  )
}