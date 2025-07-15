// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  root: 'src', // 여기서 src가 루트로 작동
  build: {
    outDir: '../dist', // src 기준 상위 폴더에 dist 생성
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': 'http://backend-service:8000',
    },
  },
});
