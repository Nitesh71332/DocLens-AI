import {
  CheckCircle2,
  AlertTriangle,
  ShieldAlert,
  ShieldCheck,
  HelpCircle,
  FileText,
  ChevronDown,
  GitCompare,
  Sparkles,
  Info,
} from 'lucide-react'
import { VERDICTS } from '../verdicts'
import ConflictGroup from './ConflictGroup'

function VerdictIcon({ verdict }) {
  const icons = {
    CONFIRMED: ShieldCheck,
    CONFLICT: ShieldAlert,
    SUPERSEDED: GitCompare,
    UNCERTAIN: HelpCircle,
    NOT_FOUND: FileText,
  }

  const Icon = icons[verdict] || HelpCircle

  return <Icon size={19} strokeWidth={2.2} />
}

function EvidenceIcon({ score }) {
  if (score >= 75) return <CheckCircle2 size={15} />
  if (score >= 50) return <ShieldCheck size={15} />
  return <AlertTriangle size={15} />
}

function formatScore(result) {
  const strength = String(result?.evidence_strength || '').toUpperCase()

  if (strength === 'STRONG') return 'Strong'
  if (strength === 'MODERATE') return 'Moderate'
  if (strength === 'WEAK') return 'Weak'
  if (strength === 'NONE') return 'None'

  const score = Number(result?.evidence_score) || 0

  if (score >= 85) return 'Very strong'
  if (score >= 70) return 'Strong'
  if (score >= 50) return 'Moderate'
  if (score >= 30) return 'Limited'

  return 'Weak'
}

export default function AnswerCard({ result }) {
  const verdict = result?.verdict || 'UNCERTAIN'
  const v = VERDICTS[verdict] || VERDICTS.UNCERTAIN

  const groups = result?.conflict?.groups || []

  const conflictVerdict =
    verdict === 'CONFLICT' || verdict === 'SUPERSEDED'

  const shownGroups = groups.filter(
    (group) =>
      group.status ===
      (conflictVerdict ? 'detected' : 'possible'),
  )

  const score = Number(result?.evidence_score) || 0
  const citations = result?.citations || []
  const evidenceCount = citations.length

  const isConflict = verdict === 'CONFLICT'
  const isSuperseded = verdict === 'SUPERSEDED'
  const isUncertain = verdict === 'UNCERTAIN'
  const isNotFound = verdict === 'NOT_FOUND'

  return (
    <article
      className="answer-card-pro"
      style={{ '--accent': v.color }}
    >
      <div className="answer-card-accent" />

      <div className="answer-question">
        <div className="question-label">
          <Sparkles size={13} />
          INVESTIGATED QUESTION
        </div>

        <div className="question-text">
          {result?.question}
        </div>
      </div>

      <div className="answer-verdict-header">
        <div className="verdict-main">
          <div className="verdict-icon">
            <VerdictIcon verdict={verdict} />
          </div>

          <div>
            <div className="verdict-kicker">
              Investigation verdict
            </div>

            <div className="verdict-title">
              {v.label}
            </div>
          </div>
        </div>

        <div className="verdict-status">
          <span
            className="verdict-status-dot"
            style={{
              background: v.color,
              boxShadow: `0 0 12px ${v.color}`,
            }}
          />

          {verdict}
        </div>
      </div>

      <div className="answer-blurb">
        {v.blurb}
      </div>

      <section className="answer-section">
        <div className="section-label">
          <span className="section-label-line" />
          ANSWER
        </div>

        <div className="answer-main">
          {result?.answer || 'No answer returned.'}
        </div>
      </section>

      {result?.reason && (
        <section className="reason-section">
          <div className="reason-icon">
            <Info size={16} />
          </div>

          <div>
            <div className="reason-title">
              Why DocuLens reached this verdict
            </div>

            <p>{result.reason}</p>
          </div>
        </section>
      )}

      <section className="evidence-overview">
        <div className="evidence-overview-head">
          <div>
            <div className="section-label">
              <span className="section-label-line" />
              EVIDENCE STRENGTH
            </div>

            <div className="evidence-score-title">
              {formatScore(result)}
            </div>
          </div>

          <div className="evidence-score">
            <strong>{score}</strong>
            <span>/ 100</span>
          </div>
        </div>

        <div className="evidence-progress">
          <div
            className="evidence-progress-fill"
            style={{
              width: `${Math.min(
                Math.max(score, 0),
                100,
              )}%`,
            }}
          />
        </div>

        <div className="evidence-meta">
          <span>
            <EvidenceIcon score={score} />
            {result?.evidence_strength || 'Not assessed'}
          </span>

          <span>
            {evidenceCount}{' '}
            {evidenceCount === 1
              ? 'verified source'
              : 'verified sources'}
          </span>
        </div>

        <div className="evidence-disclaimer">
          This is a heuristic evidence score, not a probability
          or confidence percentage.
        </div>
      </section>

      {(isConflict || isSuperseded) &&
        shownGroups.length > 0 && (
          <section className="investigation-alert">
            <div className="alert-heading">
              <div className="alert-icon">
                {isSuperseded ? (
                  <GitCompare size={17} />
                ) : (
                  <ShieldAlert size={17} />
                )}
              </div>

              <div>
                <strong>
                  {isSuperseded
                    ? 'Conflicting information detected'
                    : 'Document conflict detected'}
                </strong>

                <span>
                  {isSuperseded
                    ? 'DocuLens found competing claims and identified a newer or authoritative value.'
                    : 'Different documents provide different values for the same fact.'}
                </span>
              </div>
            </div>

            <div className="answer-conflict-groups">
              {shownGroups.map((group, index) => (
                <ConflictGroup
                  key={`${group.topic || 'group'}-${index}`}
                  group={group}
                />
              ))}
            </div>
          </section>
        )}

      {!conflictVerdict &&
        shownGroups.length > 0 && (
          <section className="possible-conflicts">
            <div className="possible-heading">
              <AlertTriangle size={16} />

              <div>
                <strong>
                  Possible conflicting information
                </strong>

                <span>
                  These differences were detected but could
                  not be verified strongly enough to change
                  the verdict.
                </span>
              </div>
            </div>

            <div className="answer-conflict-groups">
              {shownGroups.map((group, index) => (
                <ConflictGroup
                  key={`${group.topic || 'possible'}-${index}`}
                  group={group}
                />
              ))}
            </div>
          </section>
        )}

      {isUncertain && result?.unverified_answer && (
        <section className="unverified-answer">
          <div className="unverified-heading">
            <AlertTriangle size={17} />

            <div>
              <strong>
                Unverified model output
              </strong>

              <span>
                This answer was generated as a possibility,
                but DocuLens could not confirm it against
                the source documents.
              </span>
            </div>
          </div>

          <div className="unverified-content">
            {String(result.unverified_answer)}
          </div>
        </section>
      )}

      {isNotFound && (
        <div className="not-found-notice">
          <FileText size={17} />

          <div>
            <strong>
              No supporting information found
            </strong>

            <span>
              The indexed documents do not contain enough
              evidence to answer this question.
            </span>
          </div>
        </div>
      )}

      {citations.length > 0 && (
        <section className="source-section">
          <div className="source-section-head">
            <div>
              <div className="section-label">
                <span className="section-label-line" />
                VERIFIED SOURCES
              </div>

              <div className="source-subtitle">
                Evidence directly verified against the indexed
                document text.
              </div>
            </div>

            <div className="source-count">
              {citations.length}
            </div>
          </div>

          <div className="source-list">
            {citations.map((citation, index) => (
              <div
                className="source-card"
                key={`${citation.filename}-${citation.page_number}-${index}`}
              >
                <div className="source-card-top">
                  <div className="source-number">
                    {String(index + 1).padStart(2, '0')}
                  </div>

                  <div className="source-file-icon">
                    <FileText size={16} />
                  </div>

                  <div className="source-info">
                    <strong title={citation.filename}>
                      {citation.filename}
                    </strong>

                    <span>
                      Page {citation.page_number}
                      {citation.section
                        ? ` · ${citation.section}`
                        : ''}
                    </span>
                  </div>

                  <div className="source-verified">
                    <CheckCircle2 size={13} />
                    Verified
                  </div>
                </div>

                <blockquote className="source-quote">
                  “{citation.quote}”
                </blockquote>

                <div className="source-card-footer">
                  <span>
                    <ShieldCheck size={12} />
                    Quote found in source text
                  </span>

                  <span>
                    Source {index + 1}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {result?.trace?.length > 0 && (
        <details className="investigation-trace">
          <summary>
            <div className="trace-summary-left">
              <div className="trace-icon">
                <GitCompare size={15} />
              </div>

              <div>
                <strong>
                  Investigation trace
                </strong>

                <span>
                  See how DocuLens reached this result
                </span>
              </div>
            </div>

            <ChevronDown
              className="trace-chevron"
              size={17}
            />
          </summary>

          <div className="trace-body">
            {result.trace.map((step, index) => (
              <div
                className="trace-step"
                key={index}
              >
                <div className="trace-step-number">
                  {index + 1}
                </div>

                <div className="trace-step-line" />

                <div className="trace-step-text">
                  {step}
                </div>
              </div>
            ))}
          </div>
        </details>
      )}
    </article>
  )
}