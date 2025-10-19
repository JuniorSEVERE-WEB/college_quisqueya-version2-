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
    // Si ton site est hébergé à la racine, garde "/"
    base: "/",

    // ⚙️ Configuration du serveur local (dev)
    server: {
      port: 5173,
      open: true,
      proxy: {
        // ✅ Proxy pour appeler ton backend local Django sans erreur CORS
        "/api": {
          target: "http://127.0.0.1:8000",
          changeOrigin: true,
          secure: false,
        },
      },
    },

    // 📁 Options de build pour Render
    build: {
      outDir: "dist",
      assetsDir: "assets",
      sourcemap: !isProduction,
    },

    // ✅ Variables d’environnement
    define: {
      __APP_ENV__: JSON.stringify(mode),
    },
  };
});
