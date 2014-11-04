# -*- coding: utf-8 -*-
"""
Models to store shortened URLs.
"""
import time
import simplejson
import urllib
from couchdbkit.ext.django.schema import *
from datetime import datetime
from django.db import models
from django.conf import settings
from shorty.base_62 import dehydrate, saturate, url_normalize


class ShortUrlManager(models.Manager):
    """
    Manages the ShortUrl Model.
    """
    def get_by_code(self, code):
        """
        Gets a ShortUrl by the code
        :param code: unicode
        :return: ShortUrl
        """
        return self.get(unique_id=saturate(code))


class ShortUrl(models.Model):
    """
    Model representing a Short URL.
    """
    url = models.CharField(max_length=255, unique=True, db_index=True)
    clicks = models.IntegerField(blank=True, null=True, default=0)
    unique_id = models.IntegerField(db_index=True)

    objects = ShortUrlManager()

    @property
    def short_code(self):
        """
        Gets the short code based on the PK.
        """
        return dehydrate(self.unique_id)

    def generate_unique_id(self):
        """
        Generates a unique id for the URL. This adds padding to the PK based on time
        and a random key. This makes URLs less predictable, but does mean codes
        will be used up faster.
        """
        if not self.unique_id:
            self.unique_id = (self.pk + (int(time.time()) - settings.EPOCH_KEY)) * settings.PADDING_KEY

    def save(self, *args, **kwargs):
        """
        Normalises the URL and generates the correct unique id
        :type args: []
        :type kwargs: {}
        """
        self.url = url_normalize(self.url)
        super(ShortUrl, self).save(*args, **kwargs)
        if not self.unique_id:
            self.generate_unique_id()
        super(ShortUrl, self).save(*args, **kwargs)


class Click(Document):
    """
    Each click is stored in couchdb. This object handles the abstraction.
    """
    date = DateTimeProperty(default=datetime.utcnow)

    def __init__(self):
        super(Click, self).__init__()
        self.session_key = None

    def register(self, request):
        """
        Registers a click and stores in couchdb.
        :param request:
        """
        desired_keys = (
            'HTTP_HOST', 'HTTP_REFERER', 'HTTP_USER_AGENT', 'REMOTE_ADDR', )
        for key, value in request.META.iteritems():
            if key in desired_keys:
                setattr(self, key.lower(), value)
        self.parse_ip_data()
        self.session_key = request.session.session_key

    def parse_ip_data(self):
        """
        Parses the IP address using a geo API.
        """
        if not settings.PARSE_IP_DATA:
            return
        try:
            params = {
                'ip_address': self.remote_addr,
                'api_key': settings.GEO_IP_KEY
            }
            url = settings.GEO_IP_URL + '?' + urllib.urlencode(params)
            result = simplejson.load(urllib.urlopen(url))
            self.iso_country = result['country']['iso_country']
            self.iso_code_2 = result['country']['iso_code_2']
            self.iso_code_3 = result['country']['iso_code_3']
        except AttributeError:
            pass
