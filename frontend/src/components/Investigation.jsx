import { useEffect, useState } from 'react'
import {
  Search,
  Loader2,
  Sparkles,
  MessageSquareText,
  ShieldCheck,
  ArrowRight,
  RotateCcw,
  AlertCircle,
} from 'lucide-react'
import { investigate } from '../api'
import AnswerCard from './AnswerCard'

const SUGGESTIONS = [
  { text: "What is Rahul Kumar's annual salary?", icon: '₹' },
  { text: 'What is the probation period?', icon: '⏱' },
  { text: 'How many days of annual leave are employees entitled to?', icon: '📅' },
  { text: "What is Rahul Kumar's passport number?", icon: '🔎' },
]

export default function Investigation({
  hasDocs,
  result,
  setResult,
  autoAsk,
  clearAutoAsk,
}) {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function run(q) {
    const text = (q ?? question).trim()

    if (!text || loading) return

    if (text.length > 1000) {
      setError('Please keep the question under 1000 characters.')
      return
    }

    setQuestion(text)
    setLoading(true)
    setError('')

    try {
      const response = await investigate(text)
      setResult({
        ...response,
        question: text,
      })
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  function resetInvestigation() {
    if (loading) return

    setQuestion('')
    setResult(null)
    setError('')
  }

  useEffect(() => {
    if (!autoAsk) return

    const q = autoAsk.q

    clearAutoAsk()
    run(q)
  }, [autoAsk])

  return (
    <main className="pane investigation-panel">
      <div className="investigation-head">
        <div>
          <div className="investigation-eyebrow">
            <Sparkles size={13} />
            AI DOCUMENT INVESTIGATION
          </div>

          <h2>Investigation</h2>

          <p className="investigation-subtitle">
            Ask a question and let DocuLens trace the answer back to your
            documents.
          </p>
        </div>

        {result && !loading && (
          <button
            className="ghost investigation-reset"
            type="button"
            onClick={resetInvestigation}
          >
            <RotateCcw size={14} />
            New question
          </button>
        )}
      </div>

      <div className={`investigation-ask ${loading ? 'is-loading' : ''}`}>
        <div className="ask-icon">
          <MessageSquareText size={19} />
        </div>

        <input
          value={question}
          maxLength={1000}
          disabled={!hasDocs || loading}
          placeholder={
            hasDocs
              ? 'Ask anything about your documents…'
              : 'Upload documents to start investigating…'
          }
          onChange={(event) => {
            setQuestion(event.target.value)

            if (error) {
              setError('')
            }
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              event.preventDefault()
              run()
            }
          }}
        />

        <span className="question-length">
          {question.length}/1000
        </span>

        <button
          className="primary investigate-button"
          type="button"
          disabled={!hasDocs || loading || !question.trim()}
          onClick={() => run()}
        >
          {loading ? (
            <>
              <Loader2 className="spin" size={16} />
              Investigating
            </>
          ) : (
            <>
              <Search size={16} />
              Investigate
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="investigation-error">
          <div className="error-icon">
            <AlertCircle size={17} />
          </div>

          <div>
            <strong>Investigation failed</strong>
            <span>{error}</span>
          </div>
        </div>
      )}

      {!hasDocs && (
        <div className="investigation-empty">
          <div className="empty-orbit">
            <div className="empty-orbit-ring" />

            <div className="empty-center">
              <ShieldCheck size={25} />
            </div>
          </div>

          <div className="empty-content">
            <h3>Ready when your documents are</h3>

            <p>
              Upload one or more documents from the panel on the left.
              DocuLens will extract, index and compare their contents before
              answering.
            </p>

            <div className="empty-features">
              <span>
                <ShieldCheck size={13} />
                Evidence grounded
              </span>

              <span>
                <Search size={13} />
                Source verified
              </span>

              <span>
                <Sparkles size={13} />
                Conflict aware
              </span>
            </div>
          </div>
        </div>
      )}

      {hasDocs && !result && !loading && (
        <section className="suggestion-area">
          <div className="suggestion-heading">
            <div>
              <span className="suggestion-label">
                <Sparkles size={13} />
                EXAMPLE QUESTIONS
              </span>

              <p>Try one of these to get started</p>
            </div>
          </div>

          <div className="suggestion-grid">
            {SUGGESTIONS.map((suggestion) => (
              <button
                key={suggestion.text}
                className="suggestion-card"
                type="button"
                onClick={() => run(suggestion.text)}
              >
                <span className="suggestion-icon">
                  {suggestion.icon}
                </span>

                <span className="suggestion-text">
                  {suggestion.text}
                </span>

                <ArrowRight
                  className="suggestion-arrow"
                  size={15}
                />
              </button>
            ))}
          </div>
        </section>
      )}

      {loading && (
        <div className="investigation-loading">
          <div className="loading-visual">
            <div className="loading-ring ring-one" />
            <div className="loading-ring ring-two" />

            <div className="loading-core">
              <Search size={22} />
            </div>
          </div>

          <div className="loading-content">
            <strong>
              Investigating your documents
            </strong>

            <span>
              Retrieving relevant passages, comparing claims and
              verifying source evidence…
            </span>

            <div className="loading-steps">
              <span className="active">Retrieve</span>
              <span>→</span>
              <span>Compare</span>
              <span>→</span>
              <span>Verify</span>
            </div>
          </div>
        </div>
      )}

      {!loading && result && (
        <div className="investigation-result">
          <div className="result-topline">
            <div className="result-found">
              <span className="result-pulse" />
              Investigation complete
            </div>

            {result.verdict && (
              <span className="result-verdict-mini">
                {result.verdict}
              </span>
            )}
          </div>

          <AnswerCard result={result} />
        </div>
      )}
    </main>
  )
}