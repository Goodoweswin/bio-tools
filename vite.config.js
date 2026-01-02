import { defineConfig } from 'vite';
import { resolve } from 'path';
import htmlInject from 'vite-plugin-html-inject';

export default defineConfig({
  root: 'src',
  publicDir: '../public',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/index.html'),
        research: resolve(__dirname, 'src/research.html'),
        publications: resolve(__dirname, 'src/publications.html'),
        tools: resolve(__dirname, 'src/tools.html'),
        knowledge: resolve(__dirname, 'src/knowledge.html'),
        // Add other pages here as needed
      },
    },
  },
  plugins: [
    htmlInject(),
  ],
});
