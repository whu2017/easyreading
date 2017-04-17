# -*- coding: utf-8 -*-

"""
Django settings for easyreading project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from __future__ import unicode_literals
import datetime
import os

from kombu import Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ppr@22h0uc+#v13ufv&(zt381sih7k!c=)gh#y46pb+rjw%hx0'

# SECURITY WARNING: don't run with debug turned on in production!
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

    'rest_framework',  # Django Rest Framework
    'corsheaders',

    'users',
    'app.index',
    'app.transform',
    'app.deposit',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'easyreading.urls'

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

WSGI_APPLICATION = 'easyreading.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# User
AUTH_USER_MODEL = 'users.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "resource"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_QUEUES = (
    Queue(str('default'), routing_key=str('default')),
)
CELERYD_TASK_TIME_LIMIT = 600
CELERY_TIMEZONE = 'Asia/Shanghai'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(name)s:%(funcName)s:%(lineno)d] [%(threadName)s:%(thread)d] [%(levelname)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(log_color)s[%(name)s:%(funcName)s:%(lineno)d] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple_with_console': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s[%(name)s:%(funcName)s:%(lineno)d] %(levelname)s %(message)s',
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple_with_console',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'lib': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'users': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Cache
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
VERIFICATION_TIMEOUT = 900  # 15 分钟验证码过期

# Convertio
CONVERTIO_API_KEY = '7b4fe6d206158d8498cbbca0e706389b'

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'EXCEPTION_HANDLER': 'lib.rest_framework.views.api_exception_handler',
}

# Django Rest Framework JWT
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

# Alibaba DAYU
DAYU_APPKEY = '23717357'.encode('utf8')
DAYU_SECRET = '9ae2a0af04f2f32ee9ab4dfbf274f72a'.encode('utf8')
DAYU_SIGNATURE = '随阅易手机阅读'.encode('utf8')
DAYU_TEMPLATE_REGISTER = 'SMS_57905074'.encode('utf8')
DAYU_TEMPLATE_UPDATE = 'SMS_57730084'.encode('utf8')
DAYU_TEMPLATE_RESET = 'SMS_57680071'.encode('utf8')

# Alibaba SMTP
SMTP_SERVER = 'smtpdm.aliyun.com'.encode('utf8')
SMTP_PORT = 465
SMTP_FROM = 'easyreading@robot.doraemonext.com'.encode('utf8')
SMTP_PASSWORD = 'Whu2017Test'.encode('utf8')

# FUNCTION
FUNCTION_REGISTER = 'register'
FUNCTION_UPDATE = 'update'
FUNCTION_RESET = 'reset'

# Django Suit
SUIT_CONFIG = {
    'ADMIN_NAME': '随阅易管理后台',
    'MENU_EXCLUDE': ('auth.group', ),
    'LIST_PER_PAGE': 30,
    'MENU': (
        '-',
        {'label': '转换器', 'icon': 'icon-leaf', 'models': (
            'app.transform.transform',
        )},
        {'label': '用户管理', 'icon': 'icon-lock', 'models': ('users.users',)},
    )
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True

try:
    from local_settings import *
except ImportError:
    pass
