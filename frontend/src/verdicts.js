export const VERDICTS = {
  CONFIRMED:  { emoji: '??', label: 'Confirmed',  color: 'var(--green)', blurb: 'Supported by quotes verified against the documents.' },
  CONFLICT:   { emoji: '??', label: 'Conflict',   color: 'var(--red)',   blurb: 'The documents disagree and none is shown to be authoritative.' },
  SUPERSEDED: { emoji: '??', label: 'Superseded', color: 'var(--sky)',   blurb: 'The documents disagree, and one indicates which value is current.' },
  UNCERTAIN:  { emoji: '??', label: 'Uncertain',  color: 'var(--amber)', blurb: 'The evidence is weak or could not be verified.' },
  NOT_FOUND:  { emoji: '?', label: 'Not found',  color: 'var(--gray)',  blurb: 'The documents do not contain this information.' },
}
