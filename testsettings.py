DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework.authtoken',
    'rest_framework_digestauth',
)

ROOT_URLCONF = 'rest_framework_digestauth.tests'

SECRET_KEY = 'DIGESTAUTH'
