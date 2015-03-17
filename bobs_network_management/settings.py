import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'a0dy6!!^4!d1ki5e4b$=u6lfnr-hzz7j!9!6khezev8ocy)k7y'
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bobs_network_management.app',
    'bobs_network_management.app.controlpanel',
    'bobs_network_management.app.snmp',
    'bobs_network_management.app.cim',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bobs_network_management.urls'
WSGI_APPLICATION = 'bobs_network_management.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'bobs_network_management/templates'),
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'bobs_network_management/static'),
)
STATIC_URL = '/static/'