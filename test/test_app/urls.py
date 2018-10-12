try:
    # django 2.0 or higher
    from django.urls import re_path
except ImportError:
    # django 1.11 or lower
    from django.conf.urls import url as re_path

from .views import mock_view

urlpatterns = [
    re_path(r'^digest-auth/$', mock_view, name='digest_auth')
]
