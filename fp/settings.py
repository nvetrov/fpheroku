"""
Django settings for fp project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import django_heroku
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from getsecret import getsecret
import os
import yaml
from django.template.context_processors import media

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dwrp9n)aon5l=xdos%!jg%&&4yar5g-(icdvj^@a1cmg-rt&_d'
# SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['*']

TEST_RUNNER = 'django_heroku.HerokuDiscoverRunner'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # Фреймворк аутентификации и моделей по умолчанию.
    'django.contrib.contenttypes',  # Django контент-типовая система (даёт разрешения, связанные с моделями).
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # add
    'accounts',
    'Products.apps.ProductsConfig',
    #  TODO Отключить debug_toolbar in PROD. Only DEV
    'debug_toolbar',
    # 'django_python3_ldap',
    'defender',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Управление сессиями между запросами
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Связывает пользователей, использующих сессии, запросами.
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'defender.middleware.FailedLoginMiddleware',

]

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
            ],
        },
    },
]

WSGI_APPLICATION = 'fp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# import dj_database_url
# DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

# for test без авторизации по ldap
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# for prod:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'fp',
#         'USER': getsecret('username'),
#         'PASSWORD': getsecret('password'),
#         'HOST': getsecret('host'),
#         'PORT': getsecret('port'),
#         'CONN_MAX_AGE': 60 * 10,  # 10 minutes
#     }
# }
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru-RU'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# INTERNAL_IPS = [
#     # ...
#     '127.0.0.1',
#     # ...
# ]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'

# Суть  STATIC_ROOT собрать всю статику в  данное место после команды collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# python manage.py collectstatic  ВСЯ СТАТИКА ЗДЕСЬ fp/static

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'fp/static')]  # mkdir fp/static/*

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # mkdir "media" in project
MEDIA_URL = '/media/'

ROOT_URLCONF = 'fp.urls'

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = reverse_lazy('home')  # будет перемещён пользователь после удачной авторизации.
#
LOGOUT_REDIRECT_URL = reverse_lazy('login')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication.AuthBackend',
]

AUTH_USER_MODEL = 'accounts.CustomUser'
# TODO НЕ выводит ошибку, если не использовать LDAP.
#  Security DEFENDER
DEFENDER_LOCKOUT_TEMPLATE = 'defender_lockout.html'
# Колчиство попыток авторизации
DEFENDER_LOGIN_FAILURE_LIMIT = 3
DEFENDER_COOLOFF_TIME = 200  # . [Default: 300]
DEFENDER_ACCESS_ATTEMPT_EXPIRATION = 2  # hour  Пепеписывается база через 24.
# DEFENDER_DISABLE_IP_LOCKOUT = True
DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    },
}

# Activate Django-Heroku.
django_heroku.settings(locals())
