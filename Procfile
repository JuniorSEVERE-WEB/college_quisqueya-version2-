release: python backend/manage.py migrate --noinput
web: python backend/manage.py collectstatic --noinput && exec gunicorn --pythonpath backend backend.wsgi:application --timeout 120 --workers 2
