from pathlib import Path
import os
import environ
import dj_database_url
import shutil

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file if it exists
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-m+p2-=#$(r387lto-947g#hb+3t!)+3(vbfrkpt44@qbc+ep$2')

# Set DEBUG to True for debugging the 500 error
DEBUG = True

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

# Database Setup
# If DATABASE_URL is set (e.g. Postgres on Vercel), it uses that.
# Otherwise, it falls back to SQLite in /tmp for serverless persistence.
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# SQLite Vercel Workaround: Redirect to /tmp at runtime if using SQLite
if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    db_path = '/tmp/db.sqlite3'
    template_db = os.path.join(BASE_DIR, 'db_template.sqlite3')
    
    if not os.path.exists(db_path):
        try:
            if os.path.exists(template_db):
                shutil.copy2(template_db, db_path)
                os.chmod(db_path, 0o666)
            else:
                # Create empty file
                with open(db_path, 'w') as f:
                    pass
        except Exception as e:
            print(f"Error initializing sqlite file: {e}")
            
    DATABASES['default']['NAME'] = db_path


# Disconnect last_login to prevent DB writes on login for SQLite stability
try:
    from django.contrib.auth.models import update_last_login
    from django.contrib.auth.signals import user_logged_in
    user_logged_in.disconnect(update_last_login)
except:
    pass

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

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.WhiteNoiseStorage",
    },
}

# Vercel-friendly Session Engine
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.now.sh',
    'https://trip-app-gules.vercel.app'
]
