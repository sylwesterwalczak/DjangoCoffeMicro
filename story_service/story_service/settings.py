"""
Django settings for story_service project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1nfbr-&1&s8*^-40jp-gx+icffyjl99v8rap!%o#mr8lf7k98h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'storydjango']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authx',
    'corsheaders', 
    'rest_framework',
    'story',
    'pika'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authx.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'story.middleware.LogRestMiddleware',
]

ROOT_URLCONF = 'story_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'story_service.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME_STORY'),
        'USER': os.environ.get('POSTGRES_USER_STORY'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD_STORY'),
        'HOST': os.environ.get('POSTGRES_HOST_STORY'),
        'PORT': os.environ.get('POSTGRES_PORT_STORY'),
    },
    'primary_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME_AUTH'),
        'USER': os.environ.get('POSTGRES_USER_AUTH'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD_AUTH'),
        'HOST': os.environ.get('POSTGRES_HOST_AUTH'),
        'PORT': os.environ.get('POSTGRES_PORT_AUTH'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_TABLE = 'authx_customuser' 
SERVICE_API = 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpZCI6IDEsICJleHAiOiAiMjAyMi0wNC0xMyAxODowNjoxMS44NTE3NDYiLCAiaWF0IjogIjIwMjItMDQtMTMgMTc6MDY6MTEuODUxNzU0In0=.NjNlMDQzMWNjMjdhOTM5MWY0ZjY0MzQ5MGFhMGJjOTYxZWI4ZDUzYzMwNzA3YWYzZDBhZDI2Yzk0MzM3YmY3Yg==' 
AUTH_USER_MODEL = 'authx.CustomUser' 

AUTH_DB = 'primary_db'

DATABASE_ROUTERS = ['authx.dbrouter.AuthRouter']
AUTH_SERVER_PREFIX = "http://{}/rest-api/v1/authx".format(os.environ.get('AUTH_SERVER_HOST'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s | %(funcName)s | %(name)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'logstash',
            'port': 5000,  # Default value: 5959
            'version': 1,
            'message_type': 'logstash',
            'fqdn': False,
        },
    },
    'loggers': {
        'django': {
          'handlers': ['logstash'],
          'level': 'WARNING',
          'propagate': True,
      },
    }
}