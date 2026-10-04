import { useEffect, useState } from 'react'
import {
  AlertTriangle,
  CheckCircle2,
  Loader2,
  RefreshCw,
  Search,
  ShieldAlert,
  Sparkles,
  FileWarning,
} from 'lucide-react'
import { getConflicts } from '../api'
import ConflictGroup from './ConflictGroup'

export default function ConflictCenter({
  version,
  hasDocs,
  onInvestigate,
}) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function load() {
    if (!hasDocs) {
      setData(null)
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await getConflicts()
      setData(response)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [version])

  const groups = data?.groups || []

  const detected = groups.filter(
    (group) => group.status === 'detected',
  )

  const possible = groups.filter(
    (group) => group.status === 'possible',
  )

  const total = groups.length

  return (
    <main className="conflict-center">

      {/* HEADER */}
      <div className="conflict-center-head">

        <div>

          <div className="conflict-center-eyebrow">
            <Sparkles size={13} />
            DOCUMENT CONSISTENCY
          </div>

          <h2>
            Conflict Center
          </h2>

          <p>
            Compare conflicting claims across your documents
            and identify information that may need review.
          </p>

        </div>

        <button
          className="conflict-refresh"
          type="button"
          disabled={loading || !hasDocs}
          onClick={load}
        >
          <RefreshCw
            size={15}
            className={loading ? 'spin' : ''}
          />

          {loading ? 'Scanning…' : 'Refresh'}
        </button>

      </div>

      {/* SUMMARY CARDS */}
      {hasDocs && (
        <div className="conflict-summary-grid">

          <div className="conflict-summary-card total">

            <div className="conflict-summary-icon">
              <FileWarning size={17} />
            </div>

            <div>
              <strong>{total}</strong>
              <span>Total findings</span>
            </div>

          </div>

          <div className="conflict-summary-card detected">

            <div className="conflict-summary-icon">
              <ShieldAlert size={17} />
            </div>

            <div>
              <strong>{detected.length}</strong>
              <span>Confirmed conflicts</span>
            </div>

          </div>

          <div className="conflict-summary-card possible">

            <div className="conflict-summary-icon">
              <AlertTriangle size={17} />
            </div>

            <div>
              <strong>{possible.length}</strong>
              <span>Possible conflicts</span>
            </div>

          </div>

        </div>
      )}

      {/* NO DOCUMENTS */}
      {!hasDocs && (
        <div className="conflict-empty">

          <div className="conflict-empty-icon">
            <FileWarning size={24} />
          </div>

          <div>

            <h3>
              No documents to compare
            </h3>

            <p>
              Upload two or more documents to let DocuLens
              compare their claims and identify conflicting
              information.
            </p>

          </div>

        </div>
      )}

      {/* LOADING */}
      {loading && (
        <div className="conflict-loading">

          <div className="conflict-loading-icon">
            <Loader2
              size={21}
              className="spin"
            />
          </div>

          <div>

            <strong>
              Scanning for conflicts
            </strong>

            <span>
              Comparing claims across the indexed documents.
              The first scan can take a few seconds.
            </span>

          </div>

        </div>
      )}

      {/* ERROR */}
      {error && (
        <div className="conflict-error">

          <AlertTriangle size={18} />

          <div>

            <strong>
              Conflict scan failed
            </strong>

            <span>
              {error}
            </span>

          </div>

          <button
            type="button"
            onClick={load}
            disabled={loading}
          >
            Try again
          </button>

        </div>
      )}

      {/* MODEL VERIFICATION NOTICE */}
      {!loading &&
        data &&
        !data.llm_verified &&
        groups.length > 0 && (
          <div className="conflict-verification-note">

            <AlertTriangle size={15} />

            <span>
              Some conflict findings could not be confirmed
              by the language model. Review the supporting
              document evidence before treating them as final.
            </span>

          </div>
        )}

      {/* NO CONFLICTS */}
      {!loading &&
        hasDocs &&
        data &&
        groups.length === 0 && (
          <div className="conflict-success">

            <div className="conflict-success-icon">
              <CheckCircle2 size={23} />
            </div>

            <div>

              <h3>
                No conflicts detected
              </h3>

              <p>
                DocuLens did not find any verified disagreement
                between the uploaded documents.
              </p>

            </div>

          </div>
        )}

      {/* CONFLICT RESULTS */}
      {!loading &&
        groups.length > 0 && (
          <section className="conflict-results">

            <div className="conflict-results-head">

              <div>

                <div className="conflict-results-label">
                  <ShieldAlert size={13} />
                  INVESTIGATION FINDINGS
                </div>

                <h3>
                  Document differences
                </h3>

              </div>

              <span className="conflict-results-count">
                {groups.length}{' '}
                {groups.length === 1
                  ? 'finding'
                  : 'findings'}
              </span>

            </div>

            <div className="conflict-results-list">

              {groups.map((group, index) => (
                <div
                  className="conflict-result-item"
                  key={`${group.topic || 'finding'}-${index}`}
                >

                  <ConflictGroup
                    group={group}
                  />

                  <button
                    className="conflict-investigate"
                    type="button"
                    onClick={() =>
                      onInvestigate(group.topic)
                    }
                  >
                    <Search size={14} />
                    Investigate this claim
                  </button>

                </div>
              ))}

            </div>

          </section>
        )}

    </main>
  )
}