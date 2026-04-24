release: python backend/manage.py migrate --noinput && python backend/manage.py collectstatic --noinput --clear
web: gunicorn --pythonpath backend backend.wsgi:application --timeout 120 --workers 2
