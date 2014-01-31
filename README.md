# Django Rest Framework DigestAuth

[![Build Status](https://travis-ci.org/juanriaza/django-rest-framework-digestauth.png?branch=master)](https://travis-ci.org/juanriaza/django-rest-framework-digestauth)



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
