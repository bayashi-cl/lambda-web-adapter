import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/prod",
  server: {
    proxy: {
      "/prod/api": {
        target: "http://localhost:8000"
      }
    }
  }
})
