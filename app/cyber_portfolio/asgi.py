"""
ASGI config for cyber_portfolio project.
ASGI (Asynchronous Server Gateway Interface) is used for async web servers like Daphne, Uvicorn, etc.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_portfolio.settings')
application = get_asgi_application()
