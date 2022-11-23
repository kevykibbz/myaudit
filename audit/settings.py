from pathlib import Path
import environ
import os
env=environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['localhost','127.0.0.1','192.168.43.106','myauditer.herokuapp.com','www.myauditer.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'clearcache',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'installation.apps.InstallationConfig',
    'errors.apps.ErrorsConfig',
    'panel.apps.PanelConfig',
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.humanize',
    'django.contrib.sites', 
    'phonenumber_field',
    'mathfilters',
]

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

ROOT_URLCONF = 'audit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'audit.site_constants.export_vars',
            ],
        },
    },
]

WSGI_APPLICATION = 'audit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#    'default': 
#             {

#                 'ENGINE': 'mysql.connector.django',
#                 'NAME':'myauditer',
#                 'USER':'root',
#                 'PASSWORD':'',
#                 'HOST':'localhost',
#                 'PORT':3306,
#                 'OPTIONS':
#                 {
#                     'autocommit':True,
#                 },
#             }
# }

DATABASES = {
    'default': 
            {

                'ENGINE': 'django.db.backends.postgresql',
                'NAME':env('DATABASE_NAME'),
                'USER':env('DATABASE_USER'),
                'PASSWORD':env('DATABASE_PASSWORD'),
                'HOST':env('DATABASE_HOST'),
                'PORT':env('DATABASE_PORT'),
            }
}

# import dj_database_url
# db_from_env=dj_database_url.config(conn_max_age=600)
# DATABASES['default'].update(db_from_env)

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
MEDIA_URL = '/media/'

if DEBUG:
    STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
else:
    STATIC_ROOT=os.path.join(BASE_DIR,'static')


MEDIA_ROOT=os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_ENGINE='django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS='default'
CACHE_TTL = 60 * 15

#cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL','redis://127.0.0.1:6379/1'),
        #"LOCATION":"redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST=env('EMAIL_HOST')
EMAIL_HOST_USER=env('EMAIL_USER')
EMAIL_HOST_PASSWORD=env('EMAIL_PASSWORD')
EMAIL_USE_TLS=True
EMAIL_PORT=587 
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER

#login
LOGIN_URL='/accounts/login/'
LOGIN_REDIRECT_URL='/dashboard'
LOGOUT_REDIRECT_URL='/accounts/login/'