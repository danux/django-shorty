import random
import simplejson, urllib
from datetime import datetime

from django.db import models
from django.conf import settings

from couchdbkit.ext.django.schema import *

from shorty.base_62 import dehydrate, saturate, url_normalize


class ShortUrlManager(models.Manager):

    def get_by_code(self, code):
        return self.get(unique_id=saturate(code))

class ShortUrl(models.Model):

    url = models.CharField(max_length=255, unique=True, db_index=True)
    clicks = models.IntegerField(blank=True, null=True, default=0)
    unique_id = models.IntegerField(db_index=True, unique=True)

    objects = ShortUrlManager()

    @property
    def short_code(self):
        return dehydrate(self.unique_id)

    def generate_unique_id(self):
        while not self.unique_id:
            unique_id = random.getrandbits(30)
            try:
                ShortUrl.objects.get(unique_id=unique_id)
            except ShortUrl.DoesNotExist:
                self.unique_id = unique_id
            else:
                self.generate_unique_id()

    def save(self, *args, **kwargs):
        self.url = url_normalize(self.url)
        if not self.unique_id:
            self.generate_unique_id()
        super(ShortUrl, self).save(*args, **kwargs)

class Click(Document):
    date = DateTimeProperty(default=datetime.utcnow)

    def register(self, request):
        desired_keys = ('HTTP_HOST', 'HTTP_REFERER', 'HTTP_USER_AGENT', 'REMOTE_ADDR', )
        for key, value in request.META.iteritems():
            if key in desired_keys:
                setattr(self, key.lower(), value)
        self.parse_ip_data()
        self.session_key = request.session.session_key

    def parse_ip_data(self):
        if not settings.PARSE_IP_DATA:
            return
        try:
            params = {
                'ip_address': self.remote_addr,
                'api_key' : settings.GEO_IP_KEY
            }
            url = settings.GEO_IP_URL + '?' + urllib.urlencode(params)
            print url
            result = simplejson.load(urllib.urlopen(url))
            self.iso_country = result['country']['iso_country']
            self.iso_code_2 = result['country']['iso_code_2']
            self.iso_code_3 = result['country']['iso_code_3']
        except AttributeError:
            pass