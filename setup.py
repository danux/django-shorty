# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Used to install as a Python package.
"""
from distutils.core import setup

setup(
    name='django-shorty',
    version='1.0',
    description='URL shortening app for Django projects',
    author='Daniel Davies',
    author_email='daniel@danux.co.uk',
    url='https://github.com/danux/standalone-url-shortener',
    packages=['shorty', 'shorty.templatetags', ],
    install_requires=['simplejson', 'couchdbkit', 'urlnorm']
)
