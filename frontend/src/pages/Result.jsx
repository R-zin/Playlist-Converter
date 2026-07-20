import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { CopyIcon, CheckIcon, ExternalLinkIcon, ArrowRightIcon } from '../components/icons.jsx'

export default function Result() {
  const location = useLocation()
  const [copied, setCopied] = useState(false)
  const data = location.state

  if (!data) {
    return (
      <section className="max-w-[640px] mx-auto px-6 py-32 text-center">
        <h1 className="clash text-4xl md:text-5xl tracking-tight mb-8">No result yet.</h1>
        <p className="text-muted mb-10">Start a conversion to see its result here.</p>
        <Link to="/convert" className="pill-button px-12 py-5 text-lg">
          Convert a playlist
          <ArrowRightIcon />
        </Link>
      </section>
    )
  }

  async function copy() {
    try {
      await navigator.clipboard.writeText(data.url)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      /* clipboard unavailable */
    }
  }

  if (!data.ok) {
    return (
      <section className="max-w-[640px] mx-auto px-6 py-32 text-center">
        <h1 className="clash text-4xl md:text-5xl tracking-tight mb-8">Conversion failed.</h1>
        <p className="text-muted mb-10">{data.error || 'Something went wrong. Please try again.'}</p>
        <Link to="/convert" className="pill-button px-12 py-5 text-lg">
          Retry
          <ArrowRightIcon />
        </Link>
      </section>
    )
  }

  return (
    <section className="max-w-[640px] mx-auto px-6 py-32">
      <div className="flex items-center justify-center gap-3 mb-10 text-ink">
        <span className="clash text-xl">Apple Music</span>
        <span className="text-muted font-light text-2xl">→</span>
        <span className="clash text-xl">Spotify</span>
      </div>

      <h1 className="clash text-4xl md:text-5xl text-center mb-12 tracking-tight">Ready on Spotify</h1>

      {data.url ? (
        <div className="bg-surface border border-line rounded-sm p-6 flex items-center gap-4">
          <a
            href={data.url}
            target="_blank"
            rel="noreferrer"
            className="flex-grow truncate text-lg text-ink hover:text-muted transition-colors"
          >
            {data.url}
          </a>
          <button
            type="button"
            onClick={copy}
            aria-label="Copy link"
            className="text-ink hover:text-muted transition-colors shrink-0"
          >
            {copied ? <CheckIcon /> : <CopyIcon />}
          </button>
        </div>
      ) : (
        <p className="text-center text-muted mb-8">
          Your playlist was created on Spotify.
        </p>
      )}

      <div className="flex items-center justify-center gap-4 mt-10">
        {data.url && (
          <a href={data.url} target="_blank" rel="noreferrer" className="pill-button px-10 py-4 text-base">
            Open in Spotify
            <ExternalLinkIcon />
          </a>
        )}
        <Link to="/convert" className="pill-button px-10 py-4 text-base">
          Convert another
        </Link>
      </div>
    </section>
  )
}
