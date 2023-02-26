release: python manage.py migrate
web: gunicorn store_project.wsgi
worker: celery -A store_project worker --pool=solo -l info