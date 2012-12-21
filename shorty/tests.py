# -*- coding: utf-8 -*-
import unittest

from django.conf import settings
from django.test import TestCase, Client
from django.template import Context, Template

from shorty.models import ShortUrl
from shorty.base_62 import saturate, dehydrate


class TestTemplateTag(unittest.TestCase):

    def test_no_request_raises_exception(self):
        """
        Tests that the template tag raises an exception if the request is not available
        """
        context = {}
        t = Template("{% load shorty_tags %}{% short_url %}")
        c = Context(context)
        self.assertRaises(Exception, lambda: t.render(c))


class TestUrlShorten(unittest.TestCase):

    def setUp(self):
        self.url_1 = ShortUrl(url='/test-page/')
        self.url_2 = ShortUrl(url='/test-page/?query_string')
        self.url_3 = ShortUrl(url='/another-test-page/')
        self.url_4 = ShortUrl(url='http://www.a-full-url.com')

    def test_incrementing_base_62(self):
        self.url_1.save()
        self.assertEquals(self.url_1.short_code, '1')
        self.url_2.save()
        self.assertEquals(self.url_2.short_code, '2')
        self.url_3.save()
        self.assertEquals(self.url_3.short_code, '3')
        self.url_4.save()
        self.assertEquals(self.url_4.short_code, '4')


class Base62TestCase(unittest.TestCase):

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


class UrlNormalisationTestCase(unittest.TestCase):

    """ from http://www.intertwingly.net/wiki/pie/PaceCanonicalIds """
    def setUp(self):
        self.tests1 = [
            (False, "http://:@example.com/"),
            (False, "http://@example.com/"),
            (False, "http://example.com"),
            (False, "HTTP://example.com/"),
            (False, "http://EXAMPLE.COM/"),
            (False, "http://example.com/%7Ejane"),
            (False, "http://example.com/?q=%C7"),
            (False, "http://example.com/?q=%5c"),
            (False, "http://example.com/?q=C%CC%A7"),
            (False, "http://example.com/a/../a/b"),
            (False, "http://example.com/a/./b"),
            (False, "http://example.com:80/"),
            (True, "http://example.com/"),
            (True, "http://example.com/?q=%C3%87"),
            (True, "http://example.com/?q=%E2%85%A0"),
            (True, "http://example.com/?q=%5C"),
            (True, "http://example.com/~jane"),
            (True, "http://example.com/a/b"),
            (True, "http://example.com:8080/"),
            (True, "http://user:password@example.com/"),

            # from rfc2396bis
            (True, "ftp://ftp.is.co.za/rfc/rfc1808.txt"),
            (True, "http://www.ietf.org/rfc/rfc2396.txt"),
            (True, "ldap://[2001:db8::7]/c=GB?objectClass?one"),
            (True, "mailto:John.Doe@example.com"),
            (True, "news:comp.infosystems.www.servers.unix"),
            (True, "tel:+1-816-555-1212"),
            (True, "telnet://192.0.2.16:80/"),
            (True, "urn:oasis:names:specification:docbook:dtd:xml:4.1.2"),

            # other
            (True, "http://127.0.0.1/"),
            (False, "http://127.0.0.1:80/"),
            (True, "http://www.w3.org/2000/01/rdf-schema#"),
            (False, "http://example.com:081/"),
        ]

        self.tests2 = {
            '/foo/bar/.':
            '/foo/bar/',
            '/foo/bar/./':
            '/foo/bar/',
            '/foo/bar/..':
            '/foo/',
            '/foo/bar/../':
            '/foo/',
            '/foo/bar/../baz':
            '/foo/baz',
            '/foo/bar/../..':
            '/',
            '/foo/bar/../../':
            '/',
            '/foo/bar/../../baz':
            '/baz',
            '/foo/bar/../../../baz':
            '/baz',  # was: '/../baz',
            '/foo/bar/../../../../baz':
            '/baz',
            '/./foo':
            '/foo',
            '/../foo':
            '/foo',  # was: '/../foo',
            '/foo.':
            '/foo.',
            '/.foo':
            '/.foo',
            '/foo..':
            '/foo..',
            '/..foo':
            '/..foo',
            '/./../foo':
            '/foo',  # was: '/../foo',
            '/./foo/.':
            '/foo/',
            '/foo/./bar':
            '/foo/bar',
            '/foo/../bar':
            '/bar',
            '/foo//':
            '/foo/',
            '/foo///bar//':
            '/foo/bar/',
            'http://www.foo.com:80/foo':
            'http://www.foo.com/foo',
            'http://www.foo.com:8000/foo':
            'http://www.foo.com:8000/foo',
            'http://www.foo.com./foo/bar.html':
            'http://www.foo.com/foo/bar.html',
            'http://www.foo.com.:81/foo':
            'http://www.foo.com:81/foo',
            'http://www.foo.com/%7ebar':
            'http://www.foo.com/~bar',
            'http://www.foo.com/%7Ebar':
            'http://www.foo.com/~bar',
            'ftp://user:pass@ftp.foo.net/foo/bar':
            'ftp://user:pass@ftp.foo.net/foo/bar',
            'http://USER:pass@www.Example.COM/foo/bar':
            'http://USER:pass@www.example.com/foo/bar',
            'http://www.example.com./':
            'http://www.example.com/',
            '-':
            '-',
            'пример.испытание/Служебная:Search/Test':
            'http://xn--e1afmkfd.xn--80akhbyknj4f/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:Search/Test',
            'http://lifehacker.com/#!5753509/hello-world-this-is-the-new-lifehacker':
            'http://lifehacker.com/?_escaped_fragment_=5753509/hello-world-this-is-the-new-lifehacker',
        }

    def test_cases_one(self):
        for (expected, value) in self.tests1:
            short_url = ShortUrl(url=value)
            short_url.url_normalize()
            self.assertTrue((short_url.url == value)
                            == expected, (expected, value, short_url.url))

    def test_cases_two(self):
        for (original, normalised) in self.tests2.items():
            short_url = ShortUrl(url=original)
            short_url.url_normalize()
            self.assertEquals(short_url.url, normalised, (
                original, normalised, short_url.url))
