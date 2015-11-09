# -*- coding: utf-8 -*-
from django.test import TestCase, override_settings
from django.template import Context, Template
from freezegun import freeze_time

from shorty.models import ShortUrl
from shorty.base_62 import saturate, dehydrate


class TestTemplateTag(TestCase):

    def test_no_request_raises_exception(self):
        """
        Tests that the template tag raises an exception if the request is not available
        """
        context = {}
        t = Template("{% load shorty_tags %}{% short_url %}")
        c = Context(context)
        self.assertRaises(Exception, lambda: t.render(c))


class TestUrlShorten(TestCase):

    def setUp(self):
        self.url_1 = ShortUrl(url='/test-page/')
        self.url_2 = ShortUrl(url='/test-page/?query_string=True')
        self.url_3 = ShortUrl(url='/another-test-page/')
        self.url_4 = ShortUrl(url='http://www.a-full-url.com')

    @freeze_time('2000-01-01')
    @override_settings(EPOCH_KEY=946684800)
    def test_incrementing_base_62(self):
        self.url_1.save()
        self.assertEquals(self.url_1.short_code, '1')
        self.url_2.save()
        self.assertEquals(self.url_2.short_code, '2')
        self.url_3.save()
        self.assertEquals(self.url_3.short_code, '3')
        self.url_4.save()
        self.assertEquals(self.url_4.short_code, '4')


class Base62TestCase(TestCase):

    def setUp(self):
        self.tests1 = {
            0: '0',
            1: '1',
            2: '2',
            10: 'A',
            1902: 'Ug',
            1547951: '6Ugx',
            4341: '181',
            53: 'r',
            61: 'z',
        }

    def test_dehydrate(self):
        for (value, encoded) in self.tests1.items():
            self.assertEquals(encoded, dehydrate(value))

    def test_saturate(self):
        for (value, encoded) in self.tests1.items():
            self.assertEquals(value, saturate(encoded))
