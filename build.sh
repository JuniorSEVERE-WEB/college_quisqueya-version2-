#!/usr/bin/env bash
# build.sh — Script d’installation et de préparation Render (corrigé)

set -o errexit  # stoppe le script immédiatement si une commande échoue
set -o pipefail # détecte les erreurs dans les pipes
set -o nounset  # empêche l'utilisation de variables non définies

echo "🚀 Lancement du script de build pour Render..."

# Se place dans le dossier backend où se trouve manage.py
cd backend

# Installation des dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Collecte des fichiers statiques
echo "🧱 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Application des migrations
echo "🗃️  Application des migrations..."
python manage.py migrate --noinput

echo "✅ Build terminé avec succès !"
