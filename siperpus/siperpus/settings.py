"""
Django settings for siperpus project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@^!1&ec32z(^&g!y*s(18i)&lc8rcoumw(=saz=&fk!ka(#f(3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
# SESSION_FILE_PATH = '/tmp'  # Sesuaikan dengan path yang Anda inginkan

# Konfigurasi session
SESSION_COOKIE_AGE = 86400  # 24 jam dalam detik
SESSION_COOKIE_SECURE = True  # Jika menggunakan HTTPS

ALLOWED_HOSTS = [
    '8000-idx-siperpus-1730949380502.cluster-mwrgkbggpvbq6tvtviraw2knqg.cloudworkstations.dev',
    'localhost',
    '127.0.0.1'
]

CSRF_TRUSTED_ORIGINS = [
    'https://8000-idx-siperpus-1730949380502.cluster-mwrgkbggpvbq6tvtviraw2knqg.cloudworkstations.dev',
    'https://40grpvxr-8000.asse.devtunnels.ms/',
    'http://localhost:8000'
]


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000", 
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True


# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 36000
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Tambahkan konfigurasi CORS jika diperlukan
CORS_ALLOWED_ORIGINS = [
    'https://8000-idx-siperpus-1730949380502.cluster-mwrgkbggpvbq6tvtviraw2knqg.cloudworkstations.dev'
]
CORS_ALLOW_CREDENTIALS = True

TAILWIND_APP_NAME = 'theme'

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
# NPM_BIN_PATH = "/usr/local/bin/npm" # untuk linux atau macbook


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'django_browser_reload',
    'theme',
    'register',
    'rest_framework',
    'books_api',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "siperpus.middleware.LoginRequiredMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'siperpus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'siperpus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
