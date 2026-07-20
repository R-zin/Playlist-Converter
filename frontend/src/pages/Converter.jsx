import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { convertPlaylist } from '../api.js'

const APPLE_RE = /^https:\/\/music\.apple\.com\/.+\/playlist\/.+/

export default function Converter() {
  const navigate = useNavigate()
  const [url, setUrl] = useState('')
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function onSubmit(e) {
    e.preventDefault()
    setError('')
    if (!APPLE_RE.test(url.trim())) {
      setError('Enter a valid Apple Music playlist URL (https://music.apple.com/.../playlist/...).')
      return
    }
    if (!name.trim()) {
      setError('Give your new Spotify playlist a name.')
      return
    }
    setSubmitting(true)
    try {
      const { task_id } = await convertPlaylist({
        url: url.trim(),
        name: name.trim(),
        description: description.trim(),
      })
      navigate(`/progress/${encodeURIComponent(task_id)}`)
    } catch (err) {
      setError(err.message || 'Conversion failed to start.')
      setSubmitting(false)
    }
  }

  return (
    <section className="max-w-[640px] mx-auto px-6 py-24 md:py-32">
      <h1 className="clash text-4xl md:text-5xl text-center mb-12 tracking-tight">
        Paste your Apple Music playlist.
      </h1>

      <form
        onSubmit={onSubmit}
        className="bg-surface border border-line rounded-sm overflow-hidden"
      >
        <div className="p-6 border-b border-line">
          <label htmlFor="playlist_url" className="satoshi-label block mb-2">
            Apple Music playlist URL
          </label>
          <input
            id="playlist_url"
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            placeholder="https://music.apple.com/playlist/..."
            className="field"
            autoComplete="off"
          />
        </div>

        <div className="p-6 border-b border-line">
          <label htmlFor="playlist_name" className="satoshi-label block mb-2">
            Playlist Name
          </label>
          <input
            id="playlist_name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            placeholder="My Summer Mix"
            className="field"
            autoComplete="off"
          />
        </div>

        <div className="p-6">
          <label htmlFor="playlist_desc" className="satoshi-label block mb-2">
            Optional Description
          </label>
          <input
            id="playlist_desc"
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add a summary for Spotify..."
            className="field"
            autoComplete="off"
          />
        </div>

        <div className="p-6 border-t border-line">
          <button type="submit" disabled={submitting} className="pill-button w-full py-4 text-base">
            {submitting ? 'Starting…' : 'Convert'}
          </button>
        </div>
      </form>

      {error && <p className="text-center text-muted text-[14px] mt-6">{error}</p>}

      <div className="flex items-center justify-center gap-3 mt-10 text-ink">
        <span className="clash text-xl">Apple Music</span>
        <span className="text-muted font-light text-2xl">→</span>
        <span className="clash text-xl">Spotify</span>
      </div>
    </section>
  )
}
