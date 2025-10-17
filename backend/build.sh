#!/usr/bin/env bash
# build.sh — Script d’installation et de préparation Render

set -o errexit  # stoppe le script si erreur

# Installe les dépendances
pip install -r requirements.txt

# Collecte les fichiers statiques
python manage.py collectstatic --noinput

# Effectue les migrations
python manage.py migrate
