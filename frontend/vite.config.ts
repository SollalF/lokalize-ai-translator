import path from 'path';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      // Proxy all /api requests to the backend
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // Don't rewrite the path - keep the /api prefix
      },
    },
  },
});
