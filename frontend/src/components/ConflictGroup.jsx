import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
  FileText,
  GitCompare,
  ShieldAlert,
  ShieldCheck,
} from 'lucide-react'

function SourceLine({ source }) {
  return (
    <div className="conflict-source">

      <FileText size={13} />

      <span
        className="conflict-source-name"
        title={source.filename}
      >
        {source.filename}
      </span>

      <span className="conflict-source-location">
        p.{source.page}
      </span>

      {source.section && (
        <span className="conflict-source-section">
          {source.section}
        </span>
      )}

      {source.revises && (
        <span className="revision-badge">
          <Clock3 size={10} />
          Revision
        </span>
      )}

    </div>
  )
}

export default function ConflictGroup({ group }) {
  const possible =
    group.status === 'possible'

  const detected =
    group.status === 'detected'

  const resolved =
    Boolean(group.resolution)

  return (
    <article
      className={`conflict-group-pro ${
        possible ? 'is-possible' : ''
      } ${
        detected ? 'is-detected' : ''
      } ${
        resolved ? 'is-resolved' : ''
      }`}
    >

      {/* HEADER */}
      <div className="conflict-header">

        <div className="conflict-title-wrap">

          <div className="conflict-icon">

            {possible ? (
              <AlertTriangle size={17} />
            ) : resolved ? (
              <CheckCircle2 size={17} />
            ) : (
              <ShieldAlert size={17} />
            )}

          </div>

          <div>

            <div className="conflict-kicker">

              <GitCompare size={12} />

              {possible
                ? 'POSSIBLE DIFFERENCE'
                : resolved
                  ? 'CONFLICT RESOLVED'
                  : 'DOCUMENT CONFLICT'}

            </div>

            <h3>
              {group.topic || 'Related facts'}
            </h3>

          </div>

        </div>

        <div
          className={`conflict-status ${
            possible
              ? 'possible'
              : resolved
                ? 'resolved'
                : 'detected'
          }`}
        >
          {possible
            ? 'Unverified'
            : resolved
              ? 'Resolved'
              : 'Conflict'}
        </div>

      </div>

      {/* COMPARISON */}
      <div className="conflict-comparison">

        {group.positions?.map((position, index) => (
          <div
            className="conflict-position-wrap"
            key={`${position.value}-${index}`}
          >

            {index > 0 && (
              <div className="conflict-vs">
                <span>VS</span>
              </div>
            )}

            <div className="conflict-position">

              {/* VALUE */}
              <div className="conflict-value-label">
                DOCUMENT VALUE
              </div>

              <div className="conflict-value">
                {position.value}
              </div>

              {/* SOURCES */}
              {position.sources?.length > 0 && (
                <div className="conflict-sources">

                  <div className="conflict-sources-label">
                    <ShieldCheck size={12} />
                    Supporting source
                  </div>

                  {position.sources.map(
                    (source, sourceIndex) => (
                      <SourceLine
                        key={`${source.filename}-${sourceIndex}`}
                        source={source}
                      />
                    ),
                  )}

                </div>
              )}

            </div>

          </div>
        ))}

      </div>

      {/* RESOLUTION */}
      {group.resolution && (
        <div className="conflict-resolution">

          <div className="resolution-icon">
            <CheckCircle2 size={16} />
          </div>

          <div>

            <strong>
              Resolution
            </strong>

            <p>
              {group.resolution.note}
            </p>

          </div>

        </div>
      )}

      {/* UNRESOLVED MESSAGE */}
      {!possible &&
        !group.resolution && (
          <div className="conflict-unresolved">

            <ShieldAlert size={16} />

            <span>
              No document shows which value is
              authoritative.
            </span>

          </div>
        )}

      {/* REASON */}
      {group.reason && (
        <div className="conflict-reason">

          <div className="conflict-reason-label">
            Why this was flagged
          </div>

          <p>
            {group.reason}
          </p>

        </div>
      )}

      {/* POSSIBLE-CONFLICT DISCLAIMER */}
      {possible && (
        <div className="conflict-disclaimer">

          <AlertTriangle size={13} />

          <span>
            This difference was detected, but the
            available evidence was not strong enough
            to confirm a true conflict.
          </span>

        </div>
      )}

    </article>
  )
}