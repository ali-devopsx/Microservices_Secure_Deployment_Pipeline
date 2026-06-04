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

# ===== DEMO: VULNERABLE ENDPOINT (للبرزنتيشن فقط) =====
# SQL Injection عبر extra() + values()
# CVE-2024-42005: Django < 4.2.15
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q

def demo_sqli(request):
    # استخراج البيانات عبر حقن SQL في عبارة WHERE
    user_input = request.GET.get('input', '')
    
    # VULNERABLE: SQL injection عبر Q() + extra()
    # user input يذهب مباشرة لـ SQL query
    qs = User.objects.all()
    
    if user_input:
        qs = qs.extra(where=[f"username = '{user_input}' OR 1=1"])
    
    data = list(qs.values('id', 'username', 'email'))
    return JsonResponse(data, safe=False)

urlpatterns += [
    path('demo-sqli/', demo_sqli, name='demo_sqli'),
]
