#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Used to install as a Python package.
"""
from distutils.core import setup

setup(
    name='django-shorty',
    version='1.0',
    description='URL shortening app for Django projects',
    author='Daniel Davies',
    author_email='danieldavies127@gmail.com',
    url='https://github.com/danux/django-shorty',
    packages=['shorty', 'shorty.templatetags', ],
    install_requires=['urltools==0.3.2'],
)
