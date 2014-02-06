# Django Rest Framework DigestAuth

[![Build Status](https://travis-ci.org/juanriaza/django-rest-framework-digestauth.png?branch=master)](https://travis-ci.org/juanriaza/django-rest-framework-digestauth)
[![Pypi Package](https://badge.fury.io/py/djangorestframework-digestauth.png)](http://badge.fury.io/py/djangorestframework-digestauth)
[![Downloads](https://pypip.in/d/djangorestframework-digestauth/badge.png)](https://crate.io/packages/djangorestframework-digestauth/)


## Overview

This package provides [Digest Access Authentication](http://pretty-rfc.herokuapp.com/RFC2617) support for [Django REST framework](http://django-rest-framework.org/).

HTTP Digest requires the server to be able to calculate a hash over the user's username, password, and your realm.
Since `django.contrib.auth` only stores a hash of the user's password, this cannot be used to authenticate HTTP Digest sessions. This package authenticates the session against the token provided by [`TokenAuthentication`](http://django-rest-framework.org/api-guide/authentication.html#tokenauthentication).

## Installation

Install using `pip`, including any optional packages you want...

	$ pip install djangorestframework-digestauth

...or clone the project from github.

    $ git clone git@juanriaza/django-rest-framework-digestauth.git
    $ cd django-rest-framework-digestauth
    $ pip install -r requirements.txt

## How to use it?

*Check that [`TokenAuthentication`](http://django-rest-framework.org/api-guide/authentication.html#tokenauthentication) is correctly installed.*

This package provides the following authentication scheme:

- `rest_framework_digestauth.authentication.DigestAuthentication`.

Follow the [docs](http://django-rest-framework.org/api-guide/authentication.html#setting-the-authentication-scheme) to set the authentication scheme and you're all done.

## Customization

By default server-side state (specifically, the client's counter value) is
stored in the database via the [`DigestAuthCounter`](https://github.com/juanriaza/django-rest-framework-digestauth/blob/master/rest_framework_digestauth/models.py) model, and the "password"
value is stored via Django Rest Framework's TokenAuthentication backend. Both
of these things can be changed with a custom backend class. You might want to
do this if you don't like the performance characteristics of storing this kind
thing in your default database.

In order to do this, you should subclass
[`AbstractDigestBackend`](https://github.com/juanriaza/django-rest-framework-digestauth/blob/master/rest_framework_digestauth/backends.py), which has 3 methods and 1 property.

`user` - This property contains the user instance for the user attempting to authenticate. Please note that this user is not currently authenticated at this point.

`get_password()` - This should return a plain text password, or something that can be used in it's place, such as a token. Exactly what is used and how it's generated must be pre-negotiated with all clients.


`get_counter(server_nonce, client_nonce)` - This should return an integer, which should be equal to the last call to `set_counter` or `None` if there was not previously a counter set.


`set_counter(server_nonce, client_nonce, counter)` - This method should store the counter, to be returned at a later date when `get_counter` is called.

Once you've implimented a new backend, you can use it with the `DIGESTAUTH_BACKEND` setting.

    DIGESTAUTH_BACKEND = 'myapp.backends.MyDigestBackend'

## Running the tests
To run the tests against the current environment:

    $ ./manage.py test rest_framework_digestauth

## Changelog

### 1.1.0

**31th Jan 2014**

* Added Python 3 support (thanks to @defrex).

### 1.0.0

**1st Feb 2012**

* First release.
