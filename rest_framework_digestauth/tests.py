from django.contrib.auth.models import User
from django.test import Client, TestCase

from rest_framework.tests.authentication import MockView
from rest_framework.authtoken.models import Token
from rest_framework.compat import patterns

from rest_framework_digestauth.authentication import DigestAuthentication


urlpatterns = patterns('',
    (r'^digest-auth/$', MockView.as_view(authentication_classes=[DigestAuthentication])),
)

class DigestAuthTests(TestCase):
    """Digest Authentication"""

    def setUp(self):
        self.csrf_client = Client(enforce_csrf_checks=True)

        self.username = 'john'
        self.email = 'lennon@thebeatles.com'
        self.password = 'password'
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.key = 'abcd1234'
        self.token = Token.objects.create(key=self.key, user=self.user)

    def test_challenge(self):
        response = self.csrf_client.post('/digest-auth/', {'example': 'example'})
        self.assertEqual(response.status_code, 401)
        self.assertTrue('WWW-Authenticate' in response)
