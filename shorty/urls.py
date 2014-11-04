# -*- coding: utf-8 -*-
"""
The URLs file for shorty.
"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^(?P<code>[0-9A-Za-z]+)$',
                           'shorty.views.convert', name='converter'),
                       )
