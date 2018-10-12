#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Version info -- read without importing
_locals = {}
with open('rest_framework_digestauth/_version.py') as fp:
    exec(fp.read(), None, _locals)
__version__ = _locals['__version__']

setup(
    name='djangorestframework-digestauth',
    version=__version__,
    url='http://github.com/juanriaza/django-rest-framework-digestauth',
    license='BSD',
    description='Digest HTTP auth support for Django REST framework',
    author='Juan Riaza',
    author_email='juanriaza@gmail.com',
    packages=find_packages(include="rest_framework_digestauth.*"),
    include_package_data=True,
    install_requires=[
        'Django>=1.7',
        'djangorestframework',
        'six'
    ],
    tests_require=[
        'pytest',
        'pytest-django'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ]
)
