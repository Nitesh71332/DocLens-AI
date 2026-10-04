const BASE = import.meta.env.VITE_API_URL || ''

async function request(path, options = {}, timeoutMs = 120000) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)
  try {
    const res = await fetch(BASE + path, { ...options, signal: controller.signal })
    let data = null
    try { data = await res.json() } catch {}
    if (!res.ok) {
      const d = data?.detail
      const message = typeof d === 'string' ? d : Array.isArray(d) ? d.map((x) => x.msg).join('; ') : `Request failed (${res.status})`
      const err = new Error(message)
      err.status = res.status
      throw err
    }
    return data
  } catch (e) {
    if (e.name === 'AbortError') throw new Error('The request timed out. Please try again.')
    if (e instanceof TypeError) throw new Error('Cannot reach the backend. Is it running on port 8000?')
    throw e
  } finally {
    clearTimeout(timer)
  }
}

export const health = () => request('/api/health', {}, 5000)
export const listDocuments = () => request('/api/documents')
export const deleteDocument = (id) => request(`/api/documents/${id}`, { method: 'DELETE' })
export const getConflicts = () => request('/api/conflicts', {}, 180000)

export const uploadDocument = (file) => {
  const form = new FormData()
  form.append('file', file)
  return request('/api/documents/upload', { method: 'POST', body: form }, 180000)
}

export const investigate = (question) =>
  request('/api/investigate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
