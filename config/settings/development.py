"""Development settings."""
from .base import *  # noqa: F401,F403

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

# Set USE_SQLITE=True in .env for local development without MySQL
if env.bool('USE_SQLITE', default=False):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
