import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Updated: 2026-01-27
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: process.env.VITE_API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  preview: {
    port: process.env.PORT ? parseInt(process.env.PORT) : 3000,
    host: '0.0.0.0',
    strictPort: false,
    allowedHosts: [
      '.railway.app',
      'localhost',
      '127.0.0.1'
    ]
  }
})
