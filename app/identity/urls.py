"""
URL Configuration for Identity Portfolio App
This module defines URL patterns for the identity app.
Currently contains only the home page route, but can be extended with additional views.
"""

from django.urls import path
from .views import home

app_name = 'identity'

urlpatterns = [
    # Home page showing the complete portfolio
    # URL: /
    path('', home, name='home'),
]
