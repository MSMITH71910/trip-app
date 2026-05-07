from pathlib import Path
import os
import environ
import dj_database_url

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file if it exists
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-m+p2-=#$(r387lto-947g#hb+3t!)+3(vbfrkpt44@qbc+ep$2')

DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_cleanup.apps.CleanupConfig',
    'django_bootstrap5',
    'users',
    'trips',
    'itineraries',
    'budgets',
    'photos',
]

AUTH_USER_MODEL = 'users.User'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trip_planner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'trip_planner.wsgi.application'

# Database
db_url = env('DATABASE_URL', default=env('POSTGRES_URL', default=None))

if db_url:
    DATABASES = {
        'default': dj_database_url.parse(db_url)
    }
else:
    # WORKAROUND for Vercel: Use /tmp which is the only writable directory
    # Note: Data will be lost when the Vercel instance restarts
    db_path = '/tmp/db.sqlite3'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
            'OPTIONS': {
                'timeout': 20,
            }
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Modern Django 4.2+ Storage Configuration
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.WhiteNoiseStorage",
    },
}

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.now.sh',
    'https://trip-app-gules.vercel.app'
]
