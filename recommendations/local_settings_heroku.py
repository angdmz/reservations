import os
import sys

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DBNAME', 'recommendations'),
        'USER': os.getenv('DBUSER', 'recommendations'),
        'PASSWORD': os.getenv('DBPASS', 'recommendations'),
        'HOST': os.getenv('DBHOST', '127.0.0.1'),
        'PORT': os.getenv('DBPORT', '3254'),
    }
}

LOG_ROOT = os.getenv("LOG_ROOT", '/var/logs')
SECRET_KEY = os.getenv("SECRET_KEY", 'sarlanga')
FOURSQUARE_API_CLIENT_ID = os.getenv("FOURSQUARE_API_CLIENT_ID", '')
FOURSQUARE_API_CLIENT_SECRET = os.getenv("FOURSQUARE_API_CLIENT_SECRET", '')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(levelname)s %(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s',
        },
        'history': {
            'format': '%(asctime)s %(message)s'
        }
    },
    'handlers': {
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'detailed'
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_ROOT + 'info.log',
            'formatter': 'history',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_ROOT + 'error.log',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error_file', 'info_file', ],
            'level': 'WARNING',
            'propagate': True,
        },
        'logger': {
            'handlers': ['error_file', 'info_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cmd-logger': {
            'handlers': ['stdout', 'info_file', 'error_file', ],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}