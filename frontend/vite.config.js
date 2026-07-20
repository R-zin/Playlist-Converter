import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The FastAPI backend runs on :8000 by default (uvicorn main:app).
// In dev, proxy the API routes so the frontend can call same-origin paths.
const API_TARGET = process.env.VITE_API_TARGET || 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/convert': API_TARGET,
      '/status': API_TARGET,
      '/login': API_TARGET,
      '/callback': API_TARGET,
      '/healthcheck': API_TARGET,
    },
  },
})
