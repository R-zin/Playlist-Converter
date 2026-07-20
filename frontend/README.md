# Playlist-Converter — Frontend

A minimalist React front end for the Playlist-Converter API. Swiss/typographic
aesthetic, monochrome neutral, with a light/dark theme. Single direction only:
**Apple Music → Spotify**.

## Stack
- Vite + React 18 + React Router 6
- Tailwind CSS (tokens driven by CSS variables for light/dark)
- Fonts: Clash Display (headlines) + Satoshi (body) via Fontshare

## Run (dev)
```bash
npm install
npm run dev        # http://localhost:5173
```
The dev server proxies `/convert`, `/status`, `/login`, `/callback`, and
`/healthcheck` to the backend at `http://localhost:8000` (override with
`VITE_API_TARGET`). Start the FastAPI backend (`uvicorn main:app --reload`)
first.

## Build (prod)
```bash
npm run build      # outputs to dist/
npm run preview
```
For production, either serve `dist/` from the same origin as the API, or set
`VITE_API_BASE=https://your-api.example.com` so the frontend calls the API
cross-origin. You also need a **SPA fallback** (serve `index.html` for unknown
routes) and the backend CORS noted below.

## API wiring
| Page | Call |
|------|------|
| Converter | `POST /convert/apple-music-to-spotify?apple_music_playlist_url=&playlist_name=&description=` → `{ task_id, status }` |
| Progress | `GET /status/{task_id}` → `{ state, result }` (poll every 2s until terminal) |
| Result | Renders `result` on `SUCCESS`; shows error on `FAILURE` |
| Admin OAuth | `GET /login` with `X-Admin-Key` header → `{ authorization_url }` |

The converter endpoint is declared in the backend as function arguments with no
request body, so the frontend sends them as **query parameters** (matching the
generated client in `src/api.js`). If you later add a Pydantic request model,
switch `convertPlaylist` to a JSON body.

## ⚠️ Backend CORS — must be enabled for cross-origin deploys
`main.py` imports `CORSMiddleware` but never registers it (`app.add_middleware`
is missing), so the API currently sends **no CORS headers**. This is fine in
dev (Vite proxies same-origin), but a frontend served from another origin will
be blocked. Add, before `include_router(...)`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-frontend.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Theme
Light/dark tokens live in `src/index.css` (`:root` + `.dark`). The toggle is in
`src/theme.jsx`; the choice is persisted to `localStorage` and applied before
paint to avoid a flash. No accent color is used in either theme — hierarchy
comes from weight, size, and whitespace.
