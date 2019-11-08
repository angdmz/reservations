import sys

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'recommendations',
        'USER': 'recommendations',
        'PASSWORD': 'secret123',
        'HOST': '172.17.0.1',
        'PORT': '5324',
    }
}

LOG_ROOT = '/opt/project/'

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