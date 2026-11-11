import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const codespaceName = process.env.REACT_APP_CODESPACE_NAME ?? env.REACT_APP_CODESPACE_NAME ?? '';
  return {
    plugins: [react()],
    define: {
      'import.meta.env.REACT_APP_CODESPACE_NAME': JSON.stringify(codespaceName),
    },
    // Keep local API requests on the Vite origin; Codespaces uses its HTTPS forwarded port.
    server: { port: 5173, proxy: { '/api': 'http://localhost:8000' } },
    test: { environment: 'jsdom' },
  };
});
