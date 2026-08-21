"""
URL Configuration for cyber_portfolio Django Project
This module defines the root URL routing, including admin site and app URLs.
Also configures static and media file serving for development.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # Django admin site - access at /admin/
    # Log in with your superuser credentials
    path('admin/', admin.site.urls),

    # Include all identity app URLs
    # The identity app URL patterns are included here
        path('', include('identity.urls', namespace='identity')),

    # Task Manager app - requires authentication
    path('tasks/', include('tasks.urls')),

    # Authentication URLs (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

]

# ===== STATIC AND MEDIA FILES SERVING =====
# In development (when DEBUG=True), Django serves static and media files
# In production, use a web server like Nginx or Apache to serve these files

if settings.DEBUG:
    # Serve static files using staticfiles finders (development-only)
    urlpatterns += staticfiles_urlpatterns()

    # Serve media files (uploaded project images)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
