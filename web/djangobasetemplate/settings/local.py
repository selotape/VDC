"""
This is an example settings/local.py file.
These settings overrides what's in settings/base.py
"""

from . import base


# To extend any settings from settings/base.py here's an example.
# If you don't need to extend any settings from base.py, you do not need
# to import base above
INSTALLED_APPS = base.INSTALLED_APPS + ('django_nose',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vdcdbinstance',
        'USER': 'vdcdbinstance',
        'PASSWORD': 'vdcdbinstance',
        'HOST': 'vdc-dbinstance.ccop2vgfcvfp.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}



# Recipients of traceback emails and other notifications.
ADMINS = (
    ('Ron Visbord', 'RonVisbord@gmail.com'),
    ('Liahav Eitan', 'Liahavs.Mail@Gmail.com'),
)
MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
# Debugging displays nice error messages, but leaks memory. Set this to False
# on all server instances and True only for development.
DEBUG = TEMPLATE_DEBUG = True

# Is this a development instance? Set this to True on development/master
# instances and False on stage/prod.
DEV = True

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
# Hardcoded values can leak through source control. Consider loading
# the secret key from an environment variable or a file instead.
SECRET_KEY = 'd3!p@t6f0v4)@8e@c8k3)*z%!d3pjm5*sd2o0(u1ce9gc2%y+7'

# Uncomment these to activate and customize Celery:
# CELERY_ALWAYS_EAGER = False  # required to activate celeryd
# BROKER_HOST = 'localhost'
# BROKER_PORT = 5672
# BROKER_USER = 'django'
# BROKER_PASSWORD = 'django'
# BROKER_VHOST = 'django'
# CELERY_RESULT_BACKEND = 'amqp'

## Log settings

# Remove this configuration variable to use your custom logging configuration
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'loggers': {
        'djangobasetemplate': {
            'level': "DEBUG"
        }
    }
}

INTERNAL_IPS = ('127.0.0.1')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
