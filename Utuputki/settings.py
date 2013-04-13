# -*- coding: utf-8 -*-

# Get path
import os
CONTENTDIR = os.path.dirname(__file__)
PROJECTDIR = os.path.dirname(CONTENTDIR)

# Debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Admins for logging
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'C:\\Users\\Tuomas Virtanen\\My Documents\\Aptana Studio 3 Workspace\\Utuputki\\sqlite.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Other settings
ALLOWED_HOSTS = []
TIME_ZONE = 'Europe/Helsinki'
LANGUAGE_CODE = 'fi-fi'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Files
MEDIA_ROOT = os.path.join(PROJECTDIR, 'content/media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECTDIR, 'content/static/')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(CONTENTDIR, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ki_nudr1#a2xhb5%=qe0ze2=@z&%xn5%*nsi5si=6zpqsf(r-q'

# Crispy forms stuff
CRISPY_FAIL_SILENTLY = not DEBUG
CRISPY_TEMPLATE_PACK = 'uni_form'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'Utuputki.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Utuputki.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(CONTENTDIR, 'templates/'),
)

# Apps
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'Utuputki.manager',
    'Utuputki.player',
    'crispy_forms',
    'south',
)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
