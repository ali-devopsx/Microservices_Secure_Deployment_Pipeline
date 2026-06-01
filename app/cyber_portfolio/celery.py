# celery.py

from celery import Celery
import os

# Link Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_portfolio.settings')

# Create celery app
app = Celery('cyber_portfolio')

# Load config from Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto detect tasks
app.autodiscover_tasks()
