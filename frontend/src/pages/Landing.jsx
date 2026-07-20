import { Link } from 'react-router-dom'
import { ArrowRightIcon } from '../components/icons.jsx'

const steps = [
  {
    n: 'Step 01',
    title: 'Paste your link',
    body: 'Copy the URL of any public Apple Music playlist. No need for complex export settings.',
  },
  {
    n: 'Step 02',
    title: 'We convert it',
    body: 'Our system identifies tracks and matches them precisely within the Spotify catalog.',
  },
  {
    n: 'Step 03',
    title: 'Open in Spotify',
    body: 'Get your results instantly. Your new playlist is ready to play on all your devices.',
  },
]

export default function Landing() {
  return (
    <>
      {/* Hero */}
      <section className="min-h-[90vh] flex flex-col items-center justify-center text-center px-4">
        <h1 className="clash hero-title reveal stagger-1 mb-8">Move your<br />music.</h1>
        <div className="reveal stagger-2 flex flex-col items-center gap-4">
          <div className="clash text-3xl md:text-4xl text-ink flex items-center gap-4">
            Apple Music
            <span className="text-muted font-light">→</span>
            Spotify
          </div>
          <p className="text-[14px] uppercase tracking-[0.2em] text-muted font-medium mt-4">
            One-click library synchronization
          </p>
        </div>
      </section>

      {/* How it works */}
      <section className="max-w-[1200px] mx-auto px-6 md:px-8 py-32">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-0 border border-line rounded-sm bg-surface">
          {steps.map((s, i) => (
            <div
              key={s.n}
              className={`p-12 flex flex-col gap-4 ${i < steps.length - 1 ? 'md:border-r border-line' : ''}`}
            >
              <span className="text-[12px] font-medium text-muted-2 uppercase tracking-widest">
                {s.n}
              </span>
              <h3 className="text-2xl font-bold tracking-tight">{s.title}</h3>
              <p className="text-muted text-[15px] leading-relaxed">{s.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-48 flex flex-col items-center text-center px-4">
        <h2 className="clash text-5xl md:text-7xl mb-12 tracking-tighter">Ready to switch?</h2>
        <Link to="/convert" className="pill-button px-12 py-5 text-lg">
          Convert a playlist
          <ArrowRightIcon />
        </Link>
      </section>
    </>
  )
}
