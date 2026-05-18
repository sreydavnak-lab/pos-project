"""
Django settings for posdb project.
"""

import os
from pathlib import Path
import dj_database_url  # ប្រព័ន្ធទាញទិន្នន័យ Database សម្រាប់ Render

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-#v4@pg*7%g3ce*=*c61w)8p&h9=%a)o(88cuslr9ebbxayj^zy'

# ⚠️ នៅលើម៉ាស៊ីនខ្លួនឯង True តែបើនៅលើ Render (ពេលយើងកំណត់ Env) វាទៅជា False ភ្លាមដើម្បីសុវត្ថិភាព
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# 🌐 Domain របស់ Render និង Localhost
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '.onrender.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sales', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ✅ ថែមត្រង់នេះសម្រាប់គ្រប់គ្រង Static files លើ Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'posdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'posdb.wsgi.application'


# 🗄️ DATABASE SYSTEM 
# បើនៅលើ Render វាទៅរក PostgreSQL បើនៅលើម៉ាស៊ីនផ្ទាល់ខ្លួនវារត់ SQLite ធម្មតា
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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

# 📁 STATIC & MEDIA FILES CONFIGURATION (ទម្រង់ត្រឹមត្រូវមិនដាច់កូដ)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ ប្រព័ន្ធរក្សាទុករបស់ WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# ── Auth redirects ──────────────────────────────────────────────────────────
LOGIN_REDIRECT_URL  = '/sales/products/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'