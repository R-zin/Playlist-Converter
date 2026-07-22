import { useState } from 'react'
import { getAuthorizationUrl } from '../api.js'

export default function AdminOAuth() {
  const [adminKey, setAdminKey] = useState('')
  const [authUrl, setAuthUrl] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function onSubmit(e) {
    e.preventDefault()
    setError('')
    setAuthUrl('')
    if (!adminKey.trim()) {
      setError('Enter the admin key (X-Admin-Key).')
      return
    }
    setBusy(true)
    try {
      const data = await getAuthorizationUrl(adminKey.trim())
      if (!data.authorization_url) throw new Error('No authorization URL returned.')
      console.log(data.authorization_url)
      setAuthUrl(data.authorization_url)
    } catch (err) {
      setError(err.message || 'Could not start Spotify authorization.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="max-w-[560px] mx-auto px-6 py-24 md:py-32">
      <h1 className="clash text-4xl md:text-5xl text-center mb-4 tracking-tight">
        Admin · Connect Spotify
      </h1>
      <p className="text-center text-muted mb-12 text-[15px]">
        Authorize the backend&apos;s Spotify account. This is a one-time, server-side connection.
      </p>

      <form onSubmit={onSubmit} className="bg-surface border border-line rounded-sm overflow-hidden">
        <div className="p-6">
          <label htmlFor="admin_key" className="satoshi-label block mb-2">
            Admin key (X-Admin-Key)
          </label>
          <input
            id="admin_key"
            type="password"
            value={adminKey}
            onChange={(e) => setAdminKey(e.target.value)}
            required
            placeholder="••••••••••••"
            className="field"
            autoComplete="off"
          />
        </div>

        <div className="p-6 border-t border-line">
          <button type="submit" disabled={busy} className="pill-button w-full py-4 text-base">
            {busy ? 'Requesting…' : 'Get authorization link'}
          </button>
        </div>
      </form>

      {error && <p className="text-center text-muted text-[14px] mt-6">{error}</p>}

      {authUrl && (
        <div className="mt-8 text-center">
          <a
            href={authUrl}
            target="_blank"
            rel="noreferrer"
            className="pill-button px-10 py-4 text-base inline-flex"
          >
            Authorize with Spotify
          </a>
          <p className="text-muted text-[13px] mt-6 leading-relaxed">
            After you approve, Spotify redirects back to the backend, which stores the token.
            The connection is then complete — no further action needed here.
          </p>
        </div>
      )}
    </section>
  )
}
