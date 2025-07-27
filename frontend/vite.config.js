import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'icons/*'],
      manifest: {
        name: 'RAG Chatbot',
        short_name: 'RAGBot',
        start_url: '/',
        display: 'standalone',
        background_color: '#ffffff',
        theme_color: '#2c3e50',
        icons: [
          {
            src: '/icons/RAG-BOT.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/icons/RAG-BOT.png',
            sizes: '512x512',
            type: 'image/png',
          }
        ]
      }
    })
  ],
  build: {
    outDir: '../static',
    emptyOutDir: true
  }
})
