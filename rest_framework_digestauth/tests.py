from django.test import Client, TestCase
from django.contrib.auth.models import User


class DigestAuthTests(TestCase):
    """
    Digest authentication
    """
    urls = 'rest_framework.tests.authentication'

    def setUp(self):
        self.csrf_client = Client(enforce_csrf_checks=True)
        self.username = 'john'
        self.email = 'lennon@thebeatles.com'
        self.password = 'password'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_challenge(self):
        response = self.csrf_client.post('/', {'example': 'example'})
        self.assertEqual(response.status_code, 401)
