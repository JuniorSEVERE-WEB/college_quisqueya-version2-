#!/usr/bin/env bash
# ============================================
# ✅ build.sh — Script d’installation Render
# ============================================

set -o errexit  # Stoppe le script si une commande échoue

echo "🚀 Installation des dépendances Python..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Build terminé avec succès."
