import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// =============================================================
// ⚙️ Configuration Vite pour développement & production (Render)
// =============================================================

export default defineConfig(({ mode }) => {
  const isProduction = mode === "production";

  return {
    plugins: [react()],

    // 📦 Base URL pour le déploiement sur Render
    base: "/",

    // ⚙️ Configuration du serveur local (dev) - CORRIGÉ
    server: {
      port: 5173,
      host: true, // ✅ Permet l'accès depuis l'extérieur
      open: true, // ✅ Ouvre le navigateur automatiquement
      cors: true, // ✅ Active CORS pour le développement
      proxy: {
        // ✅ Proxy pour toutes les routes API vers Django
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path,
        },
        // ✅ Proxy pour les médias
        '/media': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          secure: false,
        },
        // ✅ Proxy pour l'admin Django si nécessaire
        '/admin': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          secure: false,
        }
      }
    },

    // 📁 Options de build pour Render
    build: {
      outDir: "dist",
      assetsDir: "assets",
      sourcemap: !isProduction,
      minify: isProduction ? 'esbuild' : false,
    },

    // ✅ Prévisualisation pour la production
    preview: {
      port: 5173,
      host: true,
    },

    // ✅ Variables d'environnement
    define: {
      __APP_ENV__: JSON.stringify(mode),
    },
  };
});