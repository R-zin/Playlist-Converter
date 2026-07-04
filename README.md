# Playlist-Converter

A lightweight Python web service that parses playlists from one music streaming platform and converts them to another.

> Convert playlists between streaming platforms (e.g., Spotify → Apple Music, YouTube Music → Spotify) via a simple HTTP API or CLI.

---

## Table of contents

- [Features](#features)
- [Supported platforms](#supported-platforms)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [API](#api)
- [CLI](#cli)
- [Architecture & adapters](#architecture--adapters)
- [Development](#development)
- [Testing](#testing)
- [Docker](#docker)
- [Contributing](#contributing)
- [License](#license)
- [Maintainer](#maintainer)

---

## Features

- Parse playlist URLs or exported playlist files from a source platform
- Map and search tracks on a target platform
- Return a target platform playlist URL (or create it if credentials allow)
- Pluggable adapter architecture to add new platforms
- Lightweight HTTP API with optional CLI helper

## Supported platforms

(Adjust this list to match implemented adapters.)

- Spotify
- Apple Music
- YouTube Music

## Quickstart

Prerequisites:

- Python 3.8+
- pip
- (Optional) virtualenv or venv

Clone and install:

```bash
git clone https://github.com/R-zin/Playlist-Converter.git
cd Playlist-Converter

python -m venv .venv
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows (PowerShell)

pip install -r requirements.txt
```

Run (example using Uvicorn / FastAPI):

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Or if the project uses Flask:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

## Configuration

Store API credentials and config in environment variables or a `.env` file (do not commit secrets).

Example environment variables:

- SPOTIFY_CLIENT_ID
- SPOTIFY_CLIENT_SECRET
- SPOTIFY_REDIRECT_URI
- APPLE_MUSIC_PRIVATE_KEY (or token)
- YOUTUBE_API_KEY
- PORT (default HTTP port, e.g. 8000)
- LOG_LEVEL (INFO / DEBUG)

If using a `.env` file, use python-dotenv or your deployment secrets manager to load them.

## API

POST /convert
- Description: Convert a playlist from source → target.
- Content-Type: application/json
- Body example:

```json
{
  "source": "spotify",
  "target": "apple",
  "playlist_url": "https://open.spotify.com/playlist/...",
  "create_target": true,        // optional: create playlist on target if credentials provided
  "options": {
    "preserve_order": true,
    "match_strategy": "best"    // best | strict | fuzzy
  }
}
```

Response example (200):

```json
{
  "status": "success",
  "source": "spotify",
  "target": "apple",
  "source_playlist": {
    "id": "...",
    "title": "My Playlist",
    "track_count": 42
  },
  "target_playlist_url": "https://music.apple.com/..."
}
```

GET /health
- Returns 200 and a small JSON payload to indicate service health:
```json
{ "status": "ok" }
```

GET /formats
- Returns available source/target formats and adapters.

Adjust endpoints to match your implementation files and routes.

## CLI

(Optionally provide a CLI wrapper.)

Example:

```bash
python -m playlist_converter.cli convert \
  --source spotify \
  --target apple \
  --playlist-url "https://open.spotify.com/playlist/..."
```

## Architecture & adapters

Recommended structure:

- app/ (web service)
  - main app entry (FastAPI / Flask)
- adapters/
  - spotify_adapter.py
  - apple_adapter.py
  - youtube_adapter.py
- core/
  - converter.py     # business logic: parse, map, match, create
  - search.py        # search/matching helpers
- tests/

Adapter responsibilities:
- Authenticate to their platform
- Parse/normalize playlist metadata and track identifiers
- Search for a track on the platform given title/artist/album
- Create a playlist (optional, requires write permissions)

Make adapters small and testable; provide a fallback fuzzy-match strategy for tracks not found exact.

## Development

- Add new adapters under `adapters/` and register them in the factory used by the service.
- Keep network calls async where possible.
- Use environment variables for keys and test with sandbox credentials.
- Lint with flake8/ruff and format with black.

Recommended tools:
- pytest for tests
- httpx / aiohttp for async HTTP calls
- python-dotenv for local env loading

## Testing

- Add unit tests for:
  - playlist parsing
  - matching strategies
  - adapter search behavior (use VCR or recorded mocks to avoid live API calls)
- Run:

```bash
pytest
```

## Docker

Example Dockerfile (adjust to your actual entrypoint):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

Contributions welcome! Suggested workflow:

1. Fork the repository
2. Create a feature branch: git checkout -b feature/description
3. Write tests for new behavior
4. Open a Pull Request with a clear description

Please follow the repo's code style and test coverage guidelines.

## Security

- Never commit API keys or secrets.
- Use environment variables or secrets manager in CI/CD and production.
- If you find a vulnerability, please open a private issue or contact the maintainer.

## License

MIT

## Maintainer

R-zin

---