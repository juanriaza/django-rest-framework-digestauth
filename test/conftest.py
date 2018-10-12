def pytest_configure():
    import logging

    logging.basicConfig(level=logging.INFO)

    import os
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_app.settings'
    django.setup()
