"""
Django settings for hcde project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vt3^oi$2bgrm$a!9!@(ae$!#lf2^8%g8_qiu%44@6t3v3h^vp%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'import_export',
)

LOCAL_APPS = (
    'students',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hcde.urls'

WSGI_APPLICATION = 'hcde.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'power2polar',
        'USER': 'power2polar',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

EXPORT_DIRECTORY = "/home/power2polar/Desktop"

CITIES = [
    'APISON',
    'BAKEWELL',
    'CHATTANOOGA',
    'COLLEGEDALE',
    'EAST RIDGE',
    'GEORGETOWN',
    'HARRISON',
    'HIXSON',
    'LAKESITE',
    'LOOKOUT MOUNTAIN',
    'LUPTON CITY',
    'MC DONALD',
    'OOLTEWAH',
    'RED BANK',
    'SALE CREEK',
    'SIGNAL MOUNTAIN',
    'SODDY DAISY',
    'TRENTON',
    'JASPER',
    'DUNLAP',
    'DAYTON',
    'FLINTSTONE',
    'BRYANT',
    'BIRCHWOOD',
    'GRAYSVILLE',
    'CLEVELAND',
    'WHITWELL',
    'ROSSVILLE',
    'CHICKAMAUGA',
    'POWDER SPRINGS',
    'ROCK SPRING',
    'GRUETLI LAAGER',
    'CHARLESTON',
    'RINGGOLD',
    'LAFAYETTE',
    'SPRING CITY',
    'COHUTTA',
    'RISING FAWN',
    'SOUTH PITTSBURG'
]
