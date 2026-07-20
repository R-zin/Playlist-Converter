import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getStatus, extractSpotifyUrl } from '../api.js'

const TERMINAL = new Set(['SUCCESS', 'FAILURE', 'REVOKED'])
const STATUS_WORD = {
  PENDING: 'Pending',
  RECEIVED: 'Pending',
  STARTED: 'Working',
  PROGRESS: 'Working',
  RETRY: 'Working',
  SUCCESS: 'Ready',
  FAILURE: 'Failed',
  REVOKED: 'Stopped',
}
const FILL = { Pending: '12%', Working: '55%', Ready: '100%', Failed: '100%', Stopped: '100%' }

export default function Progress() {
  const { taskId } = useParams()
  const navigate = useNavigate()
  const [state, setState] = useState('PENDING')
  const [error, setError] = useState('')
  const doneRef = useRef(false)

  useEffect(() => {
    let active = true
    const id = setInterval(async () => {
      try {
        const res = await getStatus(taskId)
        if (!active || doneRef.current) return
        const st = (res.state || 'PENDING').toUpperCase()
        setState(st)
        if (TERMINAL.has(st)) {
          doneRef.current = true
          clearInterval(id)
          if (st === 'SUCCESS') {
            navigate('/result', {
              replace: true,
              state: { ok: true, taskId, url: extractSpotifyUrl(res.result) },
            })
          } else {
            const msg =
              (res.result && (res.result.detail || res.result.error)) ||
              'The conversion failed. Please try again.'
            navigate('/result', { replace: true, state: { ok: false, taskId, error: String(msg) } })
          }
        }
      } catch (err) {
        if (!active || doneRef.current) return
        setError(err.message || 'Could not reach the server.')
        doneRef.current = true
        clearInterval(id)
      }
    }, 2000)
    return () => {
      active = false
      clearInterval(id)
    }
  }, [taskId, navigate])

  const word = STATUS_WORD[state] || 'Working'
  const fill = FILL[word] || '30%'

  return (
    <section className="max-w-[640px] mx-auto px-6 py-32 md:py-48">
      <h1 className="clash text-4xl md:text-5xl text-center mb-12 tracking-tight">Converting</h1>

      <div className="w-full h-[2px] bg-track overflow-hidden rounded-full">
        <div
          className="h-full bg-ink transition-all duration-700 ease-swiss"
          style={{ width: fill }}
        />
      </div>

      <p className="text-center text-[14px] uppercase tracking-[0.2em] text-muted font-medium mt-8">
        {error ? error : word}
      </p>

      <div className="flex items-center justify-center gap-3 mt-12 text-ink">
        <span className="clash text-xl">Apple Music</span>
        <span className="text-muted font-light text-2xl">→</span>
        <span className="clash text-xl">Spotify</span>
      </div>
    </section>
  )
}
