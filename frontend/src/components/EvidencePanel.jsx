import {
  CheckCircle2,
  FileText,
  Search,
  ShieldCheck,
  ScanText,
  ChevronDown,
  Database,
  Quote,
  Layers3,
} from 'lucide-react'

export default function EvidencePanel({ result }) {
  if (!result) {
    return (
      <aside className="evidence-panel">

        <div className="evidence-panel-header">

          <div className="evidence-title-wrap">

            <div className="evidence-header-icon">
              <ShieldCheck size={17} />
            </div>

            <div>
              <h2>Evidence</h2>

              <p>
                Source verification
              </p>
            </div>

          </div>

          <span className="evidence-status idle">
            Waiting
          </span>

        </div>

        <div className="evidence-empty">

          <div className="evidence-empty-icon">
            <Search size={22} />
          </div>

          <h3>No investigation yet</h3>

          <p>
            Verified source quotes and retrieved passages
            will appear here after you investigate a question.
          </p>

        </div>

      </aside>
    )
  }

  const cites = result.citations || []
  const passages = result.evidence || []

  const verdict = result.verdict || 'UNCERTAIN'

  const verified =
    cites.length > 0

  const statusClass =
    verdict === 'CONFIRMED'
      ? 'confirmed'
      : verdict === 'CONFLICT'
        ? 'conflict'
        : verdict === 'SUPERSEDED'
          ? 'superseded'
          : verdict === 'NOT_FOUND'
            ? 'not-found'
            : 'uncertain'

  return (
    <aside className="evidence-panel">

      {/* HEADER */}
      <div className="evidence-panel-header">

        <div className="evidence-title-wrap">

          <div className="evidence-header-icon">
            <ShieldCheck size={17} />
          </div>

          <div>
            <h2>Evidence</h2>

            <p>
              Source verification
            </p>
          </div>

        </div>

        <span className={`evidence-status ${statusClass}`}>
          {verified
            ? `${cites.length} verified`
            : 'No verified quotes'}
        </span>

      </div>

      {/* EVIDENCE SUMMARY */}
      <div className="evidence-summary">

        <div className="evidence-summary-item">

          <div className="evidence-summary-icon">
            <Quote size={15} />
          </div>

          <div>
            <strong>
              {cites.length}
            </strong>

            <span>
              Verified quotes
            </span>
          </div>

        </div>

        <div className="evidence-summary-item">

          <div className="evidence-summary-icon">
            <Layers3 size={15} />
          </div>

          <div>
            <strong>
              {passages.length}
            </strong>

            <span>
              Retrieved passages
            </span>
          </div>

        </div>

      </div>

      {/* VERIFIED SOURCES */}
      <section className="evidence-section">

        <div className="evidence-section-heading">

          <div>

            <div className="evidence-section-label">
              <CheckCircle2 size={13} />
              VERIFIED SOURCES
            </div>

            <span>
              Quotes confirmed against source text
            </span>

          </div>

          {cites.length > 0 && (
            <span className="evidence-count">
              {cites.length}
            </span>
          )}

        </div>

        {cites.length === 0 ? (
          <div className="evidence-no-source">

            <FileText size={18} />

            <div>
              <strong>
                No verified quotes
              </strong>

              <span>
                DocuLens could not verify a direct
                supporting quote for this result.
              </span>
            </div>

          </div>
        ) : (
          <div className="verified-source-list">

            {cites.map((citation, index) => (
              <article
                className="evidence-source-card"
                key={`${citation.filename}-${citation.page_number}-${index}`}
              >

                {/* SOURCE HEADER */}
                <div className="evidence-source-top">

                  <div className="evidence-source-number">
                    {String(index + 1).padStart(2, '0')}
                  </div>

                  <div className="evidence-file-icon">
                    <FileText size={15} />
                  </div>

                  <div className="evidence-source-info">

                    <strong
                      title={citation.filename}
                    >
                      {citation.filename}
                    </strong>

                    <span>
                      Page {citation.page_number}
                      {citation.section
                        ? ` · ${citation.section}`
                        : ''}
                    </span>

                  </div>

                  <CheckCircle2
                    className="evidence-verified-icon"
                    size={15}
                  />

                </div>

                {/* QUOTE */}
                <div className="evidence-quote">

                  <Quote
                    className="evidence-quote-icon"
                    size={17}
                  />

                  <blockquote>
                    “{citation.quote}”
                  </blockquote>

                </div>

                {/* FOOTER */}
                <div className="evidence-source-footer">

                  <span>
                    <ShieldCheck size={12} />
                    Quote found in source text
                  </span>

                  <span>
                    Source {index + 1}
                  </span>

                </div>

              </article>
            ))}

          </div>
        )}

      </section>

      {/* RETRIEVED PASSAGES */}
      {passages.length > 0 && (
        <details className="retrieved-evidence">

          <summary>

            <div className="retrieved-summary-left">

              <div className="retrieved-icon">
                <Database size={15} />
              </div>

              <div>

                <strong>
                  Retrieved passages
                </strong>

                <span>
                  {passages.length} passages considered
                  during investigation
                </span>

              </div>

            </div>

            <div className="retrieved-summary-right">

              <span className="retrieved-count">
                {passages.length}
              </span>

              <ChevronDown
                className="retrieved-chevron"
                size={16}
              />

            </div>

          </summary>

          <div className="retrieved-list">

            {passages.map((passage, index) => {

              const similarity =
                Number(passage.vector_score)

              const safeSimilarity =
                Number.isFinite(similarity)
                  ? similarity
                  : 0

              return (
                <article
                  className="retrieved-passage"
                  key={
                    passage.chunk_id ??
                    `${passage.filename}-${index}`
                  }
                >

                  {/* PASSAGE HEADER */}
                  <div className="retrieved-passage-head">

                    <div className="retrieved-passage-source">

                      <FileText size={14} />

                      <strong
                        title={passage.filename}
                      >
                        {passage.filename}
                      </strong>

                      <span>
                        p.{passage.page_number}
                      </span>

                    </div>

                    <div className="similarity-badge">
                      {safeSimilarity.toFixed(2)}
                    </div>

                  </div>

                  {/* SIMILARITY */}
                  <div className="similarity-row">

                    <span>
                      Retrieval similarity
                    </span>

                    <div className="similarity-bar">

                      <div
                        className="similarity-fill"
                        style={{
                          width: `${Math.min(
                            Math.max(
                              safeSimilarity * 100,
                              0,
                            ),
                            100,
                          )}%`,
                        }}
                      />

                    </div>

                  </div>

                  {/* PASSAGE TEXT */}
                  <div className="retrieved-text">
                    {passage.text}
                  </div>

                  {/* PASSAGE META */}
                  <div className="retrieved-footer">

                    <span>
                      <Search size={11} />
                      Retrieved evidence
                    </span>

                    {passage.ocr_used && (
                      <span className="ocr-badge">
                        <ScanText size={11} />
                        OCR
                      </span>
                    )}

                    {passage.section && (
                      <span>
                        {passage.section}
                      </span>
                    )}

                  </div>

                </article>
              )
            })}

          </div>

        </details>
      )}

      {/* EVIDENCE FOOTER */}
      <div className="evidence-integrity">

        <ShieldCheck size={14} />

        <span>
          Evidence shown here comes from the documents
          retrieved and verified by DocuLens.
        </span>

      </div>

    </aside>
  )
}