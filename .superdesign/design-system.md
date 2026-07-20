# Playlist-Converter — Design System

> Aesthetic minimalism. Monochrome neutral. Swiss/typographic restraint. Built for a single-direction converter: **Apple Music → Spotify**.

---

## 1. Product Context

**What it is:** A lightweight web app that takes an Apple Music playlist URL and creates the equivalent playlist on Spotify. The backend fires an async job and the frontend polls for the result.

**Live API surface (the UI must mirror this exactly):**
- `POST /convert/apple-music-to-spotify` — body fields: `apple_music_playlist_url`, `playlist_name`, `description` → returns `{ task_id, status: "PENDING" }`
- `GET /status/{task_id}` — returns `{ state, result }`. States to handle: `PENDING` → `PROGRESS`/`STARTED` → `SUCCESS` (result = Spotify playlist URL) → `FAILURE`.
- `GET /healthcheck` → `{ status: "ok" }`

**Auth note:** Spotify connection is admin-gated on the backend and **out of scope for the UI**. The frontend assumes Spotify is already connected and shows a quiet "Spotify connected" status, not an interactive OAuth screen.

**Direction is fixed:** Apple Music → Spotify only. No source/target selectors, no platform picker. The UI is built around one arrow: Apple Music → Spotify.

---

## 2. Key Pages & User Journey (JTBD)

Single job: *"I have an Apple Music playlist; I want it on Spotify with minimal effort."*

1. **Landing** — Establish the brand and the one arrow (Apple Music → Spotify). Quiet "Spotify connected" status. 3-step explanation (Paste → We convert → Open in Spotify). CTA → Converter.
2. **Converter** — The functional core. Apple Music playlist URL field, playlist name field, optional description field, and a single "Convert" pill button. Nothing else.
3. **Progress** — Polls `/status/{task_id}`. Minimal state indicator (PENDING → working → SUCCESS). No spinners-as-decoration; a thin progress line + status word.
4. **Result** — On SUCCESS: present the resulting Spotify playlist URL as a primary link, an "Open in Spotify" pill, and a copy button. On FAILURE: a calm, single-line error with a retry.

---

## 3. Branding & Styling

### Palette (strictly neutral — no accent color, ever)
| Token | Value | Use |
|-------|-------|-----|
| `--bg` | `#f2f2f2` | Page background |
| `--surface` | `#ffffff` | Cards, inputs, raised surfaces |
| `--ink` | `#111111` | Primary text, headlines |
| `--ink-soft` | `#1e1e1e` | Borders, dividers, dark footer, hover-invert |
| `--gray-1` | `#bfbfbf` | Depth layer 1, secondary decorations |
| `--gray-2` | `#c9c9c9` | Depth layer 2 |
| `--gray-3` | `#d1d1d1` | Depth layer 3 |
| `--gray-4` | `#d9d9d9` | Depth layer 4 (faintest) |
| `--muted` | `#838282` | Secondary text |
| `--muted-2` | `#b6b5b5` | Tertiary / nav-hover text |

**Rules:**
- No brand/accent color. Hierarchy comes from weight, size, and whitespace — never hue.
- Borders are `1px solid #1e1e1e` at low opacity (`#1e1e1e/10`) for resting state; full `#1e1e1e` on hover/invert.
- Dark surfaces (footer, success-finale block) use `#1e1e1e` with `#f6f6f6` text at reduced opacity.

### Dark Mode (supported second theme — exact neutral inversion)
Dark mode is the same design with every token inverted; **no new hue is introduced.** It is selected as a second theme, not a redesign.

| Token | Value | Use |
|-------|-------|-----|
| `--bg` | `#111111` | Page background (dark) |
| `--surface` | `#1e1e1e` | Cards, inputs, raised surfaces |
| `--ink` | `#f2f2f2` | Primary text, headlines |
| `--ink-soft` (border) | `rgba(246,246,246,0.10)` (`#f6f6f6/10`) | Hairlines, dividers, input borders |
| `--gray-d1` | `#2a2a2a` | Depth layer 1 |
| `--gray-d2` | `#242424` | Depth layer 2 |
| `--gray-d3` | `#1e1e1e` | Depth layer 3 |
| `--gray-d4` | `#181818` | Depth layer 4 (faintest, near bg) |
| `--muted` | `#a8a8a8` | Secondary text |
| `--muted-2` | `#8a8a8a` | Tertiary / nav-hover text |
| footer | `#0a0a0a` bg, `#f6f6f6` text at reduced opacity | Dark footer |

**Dark-mode rules:**
- Pill buttons: `1px solid #f6f6f6`, transparent bg → on hover `background: #f6f6f6; color: #111111`.
- Text fields: `background: #1e1e1e; border: 1px solid #f6f6f6/10;` → focus `border-color: #f6f6f6`. Placeholder in `--muted`.
- Status chip dot: `#f2f2f2` (no green). Depth-layer decorations and the hero echo use `#181818`→`#2a2a2a`.
- Same Clash Display + Satoshi, same scale, same spacing, same sharp corners + pills, same 700ms `cubic-bezier(0.77,0,0.175,1)` motion. No accent color, no imagery.

### Typography
- **Display / Headlines:** `Clash Display`, weight 700, letter-spacing `-0.05em`, line-height `0.9`. Load via Fontshare CDN (`https://api.fontshare.com/v2/css?f[]=clash-display@700&f[]=satoshi@500,400&display=swap`). Fallback: `system-ui, -apple-system, sans-serif`.
- **Body / UI:** `Satoshi`, weight 500 (body), 400 (captions). Fallback: `system-ui, sans-serif`.
- **Scale:** Hero headline `clamp(48px, 11vw, 180px)`. Section headings ~`4xl`–`6xl`. Body `15–16px`. Nav/labels `14px` uppercase, letter-spacing wide.
- No serif. No decorative/italic flourishes. Pure geometric sans discipline.

### Spacing & Layout
- Generous whitespace; sections breathe. Vertical rhythm in multiples of 32px.
- Sticky header height **80px**, background `#f2f2f2` at 90% opacity with `backdrop-blur(12px)`, hairline bottom border `#1e1e1e/10`.
- Content max-width ~1200px, centered, with comfortable side gutters.
- 3-column informational grids use 32px gaps.
- Asymmetrical where it earns its place; never decorative grids for their own sake.

### Radius & Form
- Cards / inputs: `rounded-sm` (sharp, ~4px) — restrained, architectural.
- Primary buttons: **pill** (`border-radius: 9999px`).
- No drop shadows for depth; use the gray depth layers and 1px borders instead. If a shadow is unavoidable, use a single soft `0 1px 0 #1e1e1e/5`.

### Icons
- Avoid illustrative/icon fluff. If a glyph is needed (copy, external-link, arrow), use **Lucide-style thin line icons** (stroke 1.5, currentColor) and keep them monochrome.
- The brand mark is pure wordmark typography — no logo SVG.

---

## 4. Motion & Animation
- Easing: `cubic-bezier(0.77, 0, 0.175, 1)`, duration **700ms** for reveals; **120ms** for color/hover transitions.
- Hover on interactive elements: subtle `scale(1.05)` and grayscale→ink or transparent→`#ffffff` surface transitions. Keep it quiet.
- Progress indicator: a thin (2px) line that fills `#111111` over the polling duration; pair with a status word (`Pending` → `Working` → `Ready`). No bouncing spinners.
- Reveal transitions use `clip-path: inset` where imagery exists (rare here).

---

## 5. Component Patterns (reference, not extracted — brand-new project)
- **Pill button (primary):** `border: 1px solid #1e1e1e; border-radius: 9999px; background: transparent;` → on hover `background: #1e1e1e; color: #f2f2f2`. Label in Satoshi 14px uppercase, tracking-wide.
- **Text field:** `background: #ffffff; border: 1px solid #1e1e1e/10; border-radius: 4px;` → focus `border-color: #1e1e1e`. No box-shadow glow. Placeholder in `--muted`.
- **Status chip ("Spotify connected"):** small pill, 1px `#1e1e1e/10` border, 12px Satoshi muted text with a 6px `#111111` dot. No green.
- **Connected-arrow motif:** typographic "Apple Music → Spotify" using Clash Display, the arrow as a thin `→` glyph in `--muted`. No platform logos.
- **Result card:** `#ffffff` surface, 1px `#1e1e1e/10` border, the Spotify URL as a large Satoshi link in `--ink`, with "Open in Spotify" pill + copy icon button.

---

## 6. Design Constraints (NON-NEGOTIABLE)
- Fonts: **only** Clash Display + Satoshi (with system fallbacks). No other typeface.
- Colors: **only** the neutral tokens above. No accent color of any kind.
- No imagery/photos/illustrations. Typography + whitespace + hairlines only.
- Sharp corners + pills. No heavy shadows. No gradients (the gray depth layers are flat fills, not gradients).
- Every page inherits the 80px sticky header and the dark footer.
- Dark mode is the exact neutral inversion of the light tokens (see Dark Mode section): same typography, same motion, **no accent color**.
