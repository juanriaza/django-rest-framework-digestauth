import base64
import os
import time
import hashlib

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.tests.test_authentication import MockView
from rest_framework.authtoken.models import Token
from rest_framework.compat import patterns

from rest_framework_digestauth.authentication import DigestAuthentication
from rest_framework_digestauth.utils import parse_dict_header
from rest_framework_digestauth.backends import DatabaseBackend

User = get_user_model()

urlpatterns = patterns(
    '',
    (r'^digest-auth/$',
    MockView.as_view(authentication_classes=[DigestAuthentication])))


def build_basic_header(username, password):
    credentials = '%s:%s' % (username, password)
    base64_credentials = base64.b64encode(
        credentials.encode(HTTP_HEADER_ENCODING)
    ).decode(HTTP_HEADER_ENCODING)
    return 'Basic %s' % base64_credentials


def build_digest_header(username, password, challenge_header, method, path,
                        nonce_count=1, cnonce=None):
    challenge_data = parse_dict_header(challenge_header.replace('Digest ', ''))
    realm = challenge_data['realm']
    nonce = challenge_data['nonce']
    qop = challenge_data['qop']
    opaque = challenge_data['opaque']

    def md5_utf8(x):
        if isinstance(x, str):
            x = x.encode('utf-8')
        return hashlib.md5(x).hexdigest()
    hash_utf8 = md5_utf8

    KD = lambda s, d: hash_utf8("%s:%s" % (s, d))

    A1 = '%s:%s:%s' % (username, realm, password)
    A2 = '%s:%s' % (method, path)

    ncvalue = '%08x' % nonce_count

    if cnonce is None:
        seed = str(nonce_count).encode('utf-8')
        seed += nonce.encode('utf-8')
        seed += time.ctime().encode('utf-8')
        seed += os.urandom(8)
        cnonce = (hashlib.sha1(seed).hexdigest()[:16])

    noncebit = "%s:%s:%s:%s:%s" % (nonce, ncvalue, cnonce, qop, hash_utf8(A2))
    respdig = KD(hash_utf8(A1), noncebit)

    base = 'username="%s", realm="%s", nonce="%s", uri="%s", '\
           'response="%s", algorithm="MD5"'
    base = base % (username, realm, nonce, path, respdig)

    if opaque:
        base += ', opaque="%s"' % opaque
    if qop:
        base += ', qop=auth, nc=%s, cnonce="%s"' % (ncvalue, cnonce)
    return 'Digest %s' % base


class DigestAuthTests(TestCase):
    """Digest Authentication"""

    def setUp(self):
        self.csrf_client = Client(enforce_csrf_checks=True)

        self.username = 'john'
        self.email = 'lennon@thebeatles.com'
        self.password = 'password'
        self.user = User.objects.create_user(self.username,
                                             self.email,
                                             self.password)
        self.key = 'abcd1234'
        self.token = Token.objects.create(key=self.key, user=self.user)

    def test_challenge(self):
        response = self.csrf_client.post('/digest-auth/',
                                         {'example': 'example'})
        self.assertEqual(response.status_code, 401)
        self.assertTrue('WWW-Authenticate' in response)

    def test_access(self):
        response = self.csrf_client.post('/digest-auth/',
                                         {'example': 'example'})
        self.assertEqual(response.status_code, 401)
        self.assertTrue('WWW-Authenticate' in response)
        auth = build_digest_header('john',
                                   'abcd1234',
                                   response['WWW-Authenticate'],
                                   'POST',
                                   '/digest-auth/')
        response = self.csrf_client.post('/digest-auth/',
                                         {'example': 'example'},
                                         HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 200)

    def test_replay_attack(self):
        response = self.csrf_client.post('/digest-auth/')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('WWW-Authenticate' in response)

        auth_kwargs = {
            'username': 'john',
            'password': 'abcd1234',
            'challenge_header': response['WWW-Authenticate'],
            'method': 'POST',
            'path': '/digest-auth/',
            'cnonce': hashlib.sha1(os.urandom(8)).hexdigest()[:16]
        }
        auth = build_digest_header(**auth_kwargs)

        response = self.csrf_client.post('/digest-auth/',
                                         HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 200)

        response = self.csrf_client.post('/digest-auth/',
                                         HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 401)
        self.assertTrue('WWW-Authenticate' in response)

        for nonce_count in range(2, 4):
            auth = build_digest_header(nonce_count=nonce_count, **auth_kwargs)
            response = self.csrf_client.post('/digest-auth/',
                                             HTTP_AUTHORIZATION=auth)
            self.assertEqual(response.status_code, 200)

    def test_database_backend(self):
        backend = DatabaseBackend(self.user)
        self.assertTrue(backend.get_password())

        server_nonce = hashlib.sha1(os.urandom(8)).hexdigest()[:16]
        client_nonce = hashlib.sha1(os.urandom(8)).hexdigest()[:16]

        self.assertEqual(backend.get_counter(server_nonce, client_nonce), None)

        backend.set_counter(server_nonce, client_nonce, 1)
        self.assertEqual(backend.get_counter(server_nonce, client_nonce), 1)

        backend = DatabaseBackend(self.user)
        backend.set_counter(server_nonce, client_nonce, 4)
        self.assertEqual(backend.get_counter(server_nonce, client_nonce), 4)

        backend = DatabaseBackend(self.user)
        self.assertEqual(backend.get_counter(server_nonce, client_nonce), 4)

    def test_basic_access(self):
        """Test if a basic access attempt results in another 401."""
        response = self.csrf_client.post('/digest-auth/',
                                         {'example': 'example'})
        auth = build_basic_header('john', 'abcd1234')
        response = self.csrf_client.post('/digest-auth/',
                                         {'example': 'example'},
                                         HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 401)
