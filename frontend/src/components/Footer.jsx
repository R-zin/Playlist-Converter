import { Link } from 'react-router-dom'

const cols = [
  {
    title: 'Navigation',
    links: [
      { label: 'Home', to: '/' },
      { label: 'Converter', to: '/convert' },
      { label: 'Admin OAuth', to: '/admin' },
    ],
  },
  {
    title: 'Resources',
    links: [
      { label: 'Convert a playlist', to: '/convert' },
      { label: 'Check status', to: '/convert' },
      { label: 'Admin', to: '/admin' },
    ],
  },
]

export default function Footer() {
  return (
    <footer
      className="text-[#f6f6f6] pt-24 pb-12 px-6 md:px-8 border-t border-white/5"
      style={{ backgroundColor: 'var(--footer-bg)' }}
    >
      <div className="max-w-[1200px] mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-16 md:gap-8 mb-24">
          <div>
            <span className="clash text-2xl tracking-tighter block mb-6">Playlist-Converter</span>
            <p className="text-white/40 text-[14px] leading-relaxed">
              A lightweight utility for seamless music migration. Built for simplicity and speed.
            </p>
          </div>

          {cols.map((col) => (
            <div key={col.title}>
              <h4 className="text-[12px] uppercase tracking-widest text-white/40 mb-8 font-medium">
                {col.title}
              </h4>
              <ul className="flex flex-col gap-4 text-[14px]">
                {col.links.map((l) => (
                  <li key={l.label}>
                    <Link to={l.to} className="text-white/60 hover:text-white transition-colors">
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          <div>
            <h4 className="text-[12px] uppercase tracking-widest text-white/40 mb-8 font-medium">
              Platform Status
            </h4>
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-white/40" />
              <span className="text-[14px] text-white/40">All Systems Operational</span>
            </div>
          </div>
        </div>

        <div className="pt-12 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
          <span className="text-[12px] text-white/20 uppercase tracking-widest">
            © {new Date().getFullYear()} Playlist-Converter
          </span>
          <span className="text-[12px] text-white/20 uppercase tracking-widest">
            Apple Music → Spotify
          </span>
        </div>
      </div>
    </footer>
  )
}
