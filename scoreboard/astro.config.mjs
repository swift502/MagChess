import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // Replace <USER> and <REPO>
  site: 'https://swift502.github.io/MagChess/',
  // base: '/<REPO>/', // optional; set if you want explicit base
  outDir: 'dist'
});
