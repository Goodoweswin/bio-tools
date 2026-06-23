import { defineConfig } from 'vite';
import { resolve } from 'path';
import htmlInject from 'vite-plugin-html-inject';

const knowledgePages = {
  annotation: resolve(__dirname, 'src/knowledge/ai-single-cell/annotation.html'),
  batchCorrection: resolve(__dirname, 'src/knowledge/ai-single-cell/batch-correction.html'),
  grnInference: resolve(__dirname, 'src/knowledge/ai-single-cell/grn-inference.html'),
  trajectory: resolve(__dirname, 'src/knowledge/ai-single-cell/trajectory.html'),
  clinicalDecision: resolve(__dirname, 'src/knowledge/ai4med/clinical-decision.html'),
  drugScreening: resolve(__dirname, 'src/knowledge/ai4med/drug-screening.html'),
  multiOmics: resolve(__dirname, 'src/knowledge/ai4med/multi-omics.html'),
  skinImaging: resolve(__dirname, 'src/knowledge/ai4med/skin-imaging.html'),
  agingClock: resolve(__dirname, 'src/knowledge/skin-aging/aging-clock.html'),
  fibroblast: resolve(__dirname, 'src/knowledge/skin-aging/fibroblast.html'),
  hes1Klf6: resolve(__dirname, 'src/knowledge/skin-aging/hes1-klf6.html'),
  il17Signaling: resolve(__dirname, 'src/knowledge/skin-aging/il17-signaling.html'),
};

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
        ...knowledgePages,
      },
    },
  },
  plugins: [
    htmlInject(),
  ],
});
