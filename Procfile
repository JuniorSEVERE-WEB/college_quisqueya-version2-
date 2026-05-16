release: python backend/manage.py migrate --noinput
web: gunicorn --pythonpath backend backend.wsgi:application --timeout 120 --workers 2
