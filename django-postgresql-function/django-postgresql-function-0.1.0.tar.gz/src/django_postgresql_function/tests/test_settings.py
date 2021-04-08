
from os import environ

SECRET_KEY = 'test-secret-key'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get(
            'DATABASE_NAME', 'django_sql_function'
        ),
        'HOST': environ.get(
            'DATABASE_HOST', 'localhost'
        ),
        'PORT': environ.get(
            'DATABASE_PORT', '5432'
        ),
        'USER': environ.get(
            'DATABASE_USER', 'postgres'
        ),
        'PASSWORD': environ.get(
            'DATABASE_PASSWORD', 'postgres'
        ),
    }
}

INSTALLED_APPS = (
    'django_postgresql_function',
    'django_postgresql_function.tests.apps.TestConfig',
)
