"""
WSGI config for cyber_portfolio project.
WSGI (Web Server Gateway Interface) is used by production web servers like Gunicorn, uWSGI, etc.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_portfolio.settings')
application = get_wsgi_application()
