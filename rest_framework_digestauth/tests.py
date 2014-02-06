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


def build_digest_header(username, password, challenge_header, method, path):
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

    nonce_count = 1
    ncvalue = '%08x' % nonce_count
    s = str(nonce_count).encode('utf-8')
    s += nonce.encode('utf-8')
    s += time.ctime().encode('utf-8')
    s += os.urandom(8)

    cnonce = (hashlib.sha1(s).hexdigest()[:16])
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
        # self.assertEqual(response.status_code, 401)
        # self.assertTrue('WWW-Authenticate' in response)
        auth = build_digest_header('john',
                                   'abcd1234',
                                   response['WWW-Authenticate'],
                                   'POST',
                                   '/digest-auth/')
        response = self.csrf_client.post('/digest-auth/',
                                         {'example': 'example'},
                                         HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 200)

    def test_basic_access(self):
        """Test if a basic access attempt results in another 401."""
        response = self.csrf_client.post('/digest-auth/',
                                         {'example': 'example'})
        auth = build_basic_header('john', 'abcd1234')
        response = self.csrf_client.post('/digest-auth/',
                                         {'example': 'example'},
                                         HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 401)
