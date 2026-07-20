import { Link } from 'react-router-dom'
import { useTheme } from '../theme.jsx'
import { SunIcon, MoonIcon } from './icons.jsx'

export default function Header() {
  const { theme, toggle } = useTheme()

  return (
    <header className="fixed top-0 left-0 w-full h-[80px] z-50 bg-bg/90 backdrop-blur-[12px] border-b border-line px-6 md:px-8 flex items-center justify-between">
      <Link to="/" className="clash text-xl md:text-2xl tracking-tighter">
        Playlist-Converter
      </Link>

      <div className="flex items-center gap-4 md:gap-6">
        {/* Quiet connection status — backend handles auth, so this is an indicator only */}
        <div
          className="hidden sm:flex items-center gap-2 px-3 py-1.5 border border-line rounded-full"
          title="Spotify is connected on the server"
        >
          <span className="w-1.5 h-1.5 rounded-full bg-ink" />
          <span className="text-[12px] font-medium text-muted uppercase tracking-wider">
            Spotify Connected
          </span>
        </div>

        <button
          type="button"
          onClick={toggle}
          aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          className="text-ink hover:text-muted transition-colors"
        >
          {theme === 'dark' ? <SunIcon /> : <MoonIcon />}
        </button>

        <Link to="/convert" className="pill-button">
          Convert
        </Link>
      </div>
    </header>
  )
}
