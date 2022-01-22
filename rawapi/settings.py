"""
Django settings for rawapi project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from django.contrib.messages import constants as messages
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['rawfinancial.fund', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'crispy_forms',
    'authentication',
    'channel',
    'trust_network',
    'financial_institute',
    'dashboard',
    'loans',
    'borrowers',
    'wallet',
    'bootstrap_modal_forms',
    'numpy',
    'drf_yasg2',
    'rest_framework.authtoken'
    
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'authentication.authentication.ExpiringTokenAuthentication',

    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'EXCEPTION_HANDLER':'utils_api.utils.custom_exception_handler',
    'DATE_INPUT_FORMATS': ["%m %d,%Y", ]
    

}

TOKEN_EXPIRED_AFTER_SECONDS = 3600

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Token': {
            'type': 'basic'
      },
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rawapi.urls'

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

WSGI_APPLICATION = 'rawapi.wsgi.application'


AUTH_USER_MODEL = 'authentication.User'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'rawadmin',
        #'USER': 'raw-financial',
        #'PASSWORD': 'QHpfN2v6ZC_rHt2s',
        #'HOST': 'private-ortus-db-do-user-9816964-0.b.db.ondigitalocean.com',
        #'PORT': '25060',
        #'OPTIONS':{
            #'sslmode':'verify-full',
            #'sslrootcert':os.path.join(BASE_DIR, 'ca-certificate.crt')
        #}
   # }
#}


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

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'



# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

XENTE_API_KEY = config('XENTE_API_KEY', default='')

XENTE_API_KEY_RESELLER = config('XENTE_API_KEY_RESELLER', default='')

ACCOUNT_ID = config('ACCOUNT_ID', default='')

XENTE_BASE_URL_PAYMENT="http://sandbox666353.westeurope.cloudapp.azure.com:9080"

XENTE_BASE_URL_RESELLER="http://sandbox666353.westeurope.cloudapp.azure.com:8067"



XENTE_PASSWORD=config('XENTE_PASSWORD', default='')

XENTE_TOKEN=config('XENTE_TOKEN', default='')