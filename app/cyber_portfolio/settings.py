"""
Django settings for cyber_portfolio project.
This module contains all configuration settings including database, installed apps,
middleware, static/media file paths, and security settings.
For production, update DEBUG=False and set ALLOWED_HOSTS appropriately.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# In production, use environment variables to store this
SECRET_KEY = 'my_ultra_secret_production_key_2026'

# SECURITY WARNING: don't run with debug turned on in production!
# Set to False when deploying to production
DEBUG = True

# In production, add your domain here (e.g., 'example.com', 'www.example.com')
#ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,ali-devsecops-app").split(",")


# ===== INSTALLED APPS =====
# Add 'identity' app to handle the portfolio
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'identity',  # Our custom identity portfolio app
    'tasks',     # Task Manager app
]

# ===== MIDDLEWARE =====
# Standard Django middleware for handling requests/responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'cyber_portfolio.urls'

# ===== TEMPLATES =====
# Template engine configuration for rendering Django templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Add the templates directory for custom templates
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'identity.context_processors.profile_context',
            ],
        },
    },
]

# WSGI application entry point
WSGI_APPLICATION = 'cyber_portfolio.wsgi.application'

# ===== DATABASE =====
# Using SQLite database for development
# In production, switch to PostgreSQL or MySQL
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}


# Database configuration for Production (PostgreSQL)
# We fetch credentials securely from environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'cyber_db'),
        'USER': os.environ.get('DB_USER', 'cyber_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'cyber_pass'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}




# ===== PASSWORD VALIDATION =====
# Password validators for user authentication (not used in this portfolio, but good practice)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ===== INTERNATIONALIZATION =====
# Language and timezone settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ===== STATIC FILES =====
# Configuration for serving static files (CSS, JS, images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'identity', 'static'),
]

# ===== MEDIA FILES =====
# Configuration for serving uploaded files (project images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ===== DEFAULT PRIMARY KEY FIELD =====
# Use BigAutoField as default for new models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===== AUTHENTICATION SETTINGS =====
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'tasks:task_list'
LOGOUT_REDIRECT_URL = 'identity:home'


# ===== SECURITY SETTINGS =====
# These settings should be reviewed and adjusted for production
# For development, these are set to permissive values
CSRF_TRUSTED_ORIGINS = []

# In production, set these to True:
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_SECURITY_POLICY = {...}


# Unsecured Redis Cache Configuration for Testing

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://:{os.environ.get("REDIS_PASSWORD", "")}@redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}



# =========================
# Celery Configuration
# =========================

# Redis connection (message broker)
CELERY_BROKER_URL = f'redis://:{os.environ.get("REDIS_PASSWORD", "")}@redis:6379/0'

# Store task results
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Data format
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
