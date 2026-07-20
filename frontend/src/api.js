// API client for the Playlist-Converter FastAPI backend.
//
// In dev, Vite proxies these paths to the backend (see vite.config.js), so we
// call same-origin relative paths. In production, set VITE_API_BASE to the
// backend origin (e.g. https://api.example.com).
const BASE = import.meta.env.VITE_API_BASE || ''

async function asJson(res) {
  const text = await res.text()
  let data
  try {
    data = text ? JSON.parse(text) : {}
  } catch {
    data = { detail: text }
  }
  if (!res.ok) {
    const detail = data && data.detail ? data.detail : `Request failed (${res.status})`
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
  }
  return data
}

// POST /convert/apple-music-to-spotify
// The backend declares these as function args with no request body model, so
// FastAPI reads them as query parameters.
export async function convertPlaylist({ url, name, description }) {
  const params = new URLSearchParams({
    apple_music_playlist_url: url,
    playlist_name: name,
    description: description || '',
  })
  const res = await fetch(`${BASE}/convert/apple-music-to-spotify?${params.toString()}`, {
    method: 'POST',
  })
  return asJson(res) // { task_id, status }
}

// GET /status/{task_id} -> { state, result }
export async function getStatus(taskId) {
  const res = await fetch(`${BASE}/status/${encodeURIComponent(taskId)}`)
  return asJson(res)
}

// GET /login (admin-gated) -> { authorization_url }
export async function getAuthorizationUrl(adminKey) {
  const res = await fetch(`${BASE}/login`, {
    headers: { 'X-Admin-Key': adminKey },
  })
  return asJson(res)
}

// GET /healthcheck -> { status: "ok" }
export async function healthcheck() {
  const res = await fetch(`${BASE}/healthcheck`)
  return asJson(res)
}

// Normalize the Celery task result into a Spotify URL when possible.
export function extractSpotifyUrl(result) {
  if (!result) return null
  if (typeof result === 'string') return result
  if (typeof result === 'object') {
    return (
      result.url ||
      result.playlist_url ||
      result.spotify_url ||
      result.target_playlist_url ||
      null
    )
  }
  return null
}
