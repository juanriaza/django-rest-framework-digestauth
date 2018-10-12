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

MIDDLEWARE = []

ROOT_URLCONF = 'test_app.urls'

SECRET_KEY = 'DIGESTAUTH'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_digestauth.authentication.DigestAuthentication'],
    "DEFAULT_PERMISSION_CLASSES": ['rest_framework.permissions.IsAuthenticated']
}
