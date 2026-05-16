# Dockerfile pour le frontend React (Vite).
# Railway utilise prioritairement ce Dockerfile s'il existe — il contourne
# Nixpacks et toute Custom Start Command réglée dans le dashboard.

# ════════════════════════════════════════════════════════════════
#  Étape 1 — Build du bundle Vite
# ════════════════════════════════════════════════════════════════
FROM node:20-alpine AS builder
WORKDIR /app

# Installer les dépendances en premier (meilleur cache Docker)
COPY package.json package-lock.json ./
RUN npm ci

# Copier le reste du source et builder
COPY . .
RUN npm run build

# ════════════════════════════════════════════════════════════════
#  Étape 2 — Image runtime minimale qui sert dist/ via `serve`
# ════════════════════════════════════════════════════════════════
FROM node:20-alpine AS runner
WORKDIR /app

# Installation de `serve` (petit serveur statique avec fallback SPA)
RUN npm install -g serve@14

# On ne copie QUE le bundle, pas le source
COPY --from=builder /app/dist ./dist

# Railway injecte la variable PORT à l'exécution ; serve la respecte via -l.
# Le flag -s active le fallback SPA : toute route inconnue → index.html
ENV PORT=3000
EXPOSE 3000

CMD ["sh", "-c", "serve -s dist -l tcp://0.0.0.0:${PORT}"]
