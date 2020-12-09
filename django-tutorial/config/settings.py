"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wz!imx1ty=ho*d6qrkvoylag5i&7dr(cq6nbb%7m0ovo42mlsq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# if DEBUG=False, ALLOWED_HOSTS must be set (production server)
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',           # the admin site
    'django.contrib.auth',            # core authenticaton framework
    'django.contrib.contenttypes',    # content framework (model permissions)
    'django.contrib.sessions',        # session framework
    'django.contrib.messages',        # messaging framework
    'django.contrib.staticfiles',     # content management
    # OTHER RELEVANT PACKAGE INSTALLS
    'django_extensions',             # pip install django-extensions
    'rest_framework',                # pip install djangorestframework
    #'djongo',                       # requires django 3.05
    # LOCAL PROJECT APPS
    'polls',                         # dev/pip install django-polls

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # messaging
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  # messaging
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# these will force the success_url to be this whenever
# there is a successful login or logout. we are not likely
# to want to always redirect here, which is why forms need
# <input type="hidden" name="next" value="/polls/">

#LOGIN_REDIRECT_URL = "/polls/"
#LOGOUT_REDIRECT_URL = "/polls/login"
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
DEFAULT_FROM_EMAIL = "sdugaro@gmail.com"
SITE_NAME = "Django-Tutorial"
SITE_URL = "http://127.0.0.1:8000/"

# add to configure the logging module
LOGGING = {
    # dictConfig format version
    'version': 1,
    # turn off all logging when True
    'disable_existing_loggers': False,
    # define formatters:
    # simple:
    # - outputs the log level name and message. Level names right justified.
    # verbose:
    # - include time of log, module logged from and process ids.
    # file:
    # - format in columns using default '%' style tokenization
    'formatters': {
        'simple': {
            'format': '{levelname:>8s}[{module}] {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{levelname:8s} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(module)s %(levelname)-8s %(message)s'
        }
    },
    # define filters
    # any handler using this filter will only process log messges
    # when config/setting has set DEBUG=True
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # define handlers:
    # console:
    # - prints to sys.stderr using the 'simple' formatter
    # - writes DEBUG level messages and higher unless overridden
    # - logging will be turned off with Djangos shell logging
    # file:
    # - writes to the specified log file using the 'file' formatter
    # - only write INFO level messages and higher to that file.
    # - log filename will be created when server starts if DNE
    'handlers': {
        'console': {
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/polls_debug.log'
        },
        'signal_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/polls_signals.log'
        }

    },
    # define loggers:
    # polls:
    # - app logging INFO to console only. level = NOTSET = 0 by default.
    # - suppresses messages lower than DEBUG unless setLevel() override
    # polls.file
    # - app logging file at file handler level + use parent polls logging
    # polls.both
    # - app logging DEBUG to console since no level set there
    # - app logging INFO to file since handler overries level
    # - dont propagate to parent else console will print twice
    'loggers': {
        'polls': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'polls.file': {
            'handlers': ['file'],
            'propagate': True,
        },
        'polls.both': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'polls.signals': {
            'level': 'DEBUG',
            'handlers': ['console', 'signal_log'],
            'propagate': False,
        }
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR, "media", ]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

