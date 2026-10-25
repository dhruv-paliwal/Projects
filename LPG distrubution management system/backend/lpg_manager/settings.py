"""
Django settings for lpg_manager project.
Engineered for LPG Distribution & Consumer Management Dashboard.
Database: MySQL with mysql-connector-python backend.
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-r0!m_0gx0c&!_ggsz=z7b9xf&vsu4t0x!@@rk%$1)07kl%xvqo')

DEBUG = os.getenv('DEBUG', 'True').strip() == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Bespoke LPG Management App
    'dashboard.apps.DashboardConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]
try:
    import whitenoise
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
except ImportError:
    pass

MIDDLEWARE.extend([
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
])

ROOT_URLCONF = 'lpg_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.parent / 'frontend' / 'templates',
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lpg_manager.wsgi.application'

# ==============================================================================
# Database Configuration: MySQL using mysql-connector-python
# ==============================================================================
# Production/Primary specification strictly targets MySQL via 'mysql.connector.django'.
# For immediate out-of-the-box local testing, fallback to SQLite is provided when
# MySQL is unreachable or when USE_SQLITE is set.

DB_ENGINE = os.getenv('DB_ENGINE', '').strip().lower()
USE_SQLITE = os.getenv('USE_SQLITE', '').strip().lower() in ('1', 'true', 'yes')

DB_NAME = os.getenv('DB_NAME', 'lpg_manager_db').strip()
DB_USER = os.getenv('DB_USER', 'root').strip()
DB_PASSWORD = os.getenv('DB_PASSWORD', '').strip()
DB_HOST = os.getenv('DB_HOST', '127.0.0.1').strip()
DB_PORT = os.getenv('DB_PORT', '3306').strip()

def is_mysql_available():
    """Test if MySQL server is reachable with the provided credentials."""
    if USE_SQLITE or DB_ENGINE == 'sqlite':
        return False
    try:
        import mysql.connector
        cnx = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=int(DB_PORT),
            connection_timeout=2
        )
        cnx.close()
        return True
    except Exception:
        return False

# Configure the database dictionary
if not USE_SQLITE and DB_ENGINE != 'sqlite' and is_mysql_available():
    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'OPTIONS': {
                'charset': 'utf8mb4',
                'autocommit': True,
                'use_pure': True,
            },
        }
    }
else:
    # Resilient local fallback ensuring seamless migrations, tests, and demo runs
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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

# Internationalization - Indian Standard Time and Locale
LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR.parent / 'frontend' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
