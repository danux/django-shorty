# -*- coding: utf-8 -*-
"""
Models to store shortened URLs.
"""
from django.db import models
import urltools
from shorty.base_62 import dehydrate, saturate


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
    unique_id = models.IntegerField(db_index=True, null=True)

    objects = ShortUrlManager()

    @property
    def short_code(self):
        """
        Gets the short code based on the PK.
        """
        return dehydrate(self.id)

    def save(self, *args, **kwargs):
        """
        Normalises the URL and generates the correct unique id
        :type args: []
        :type kwargs: {}
        """
        self.url = urltools.normalize(self.url)
        super(ShortUrl, self).save(*args, **kwargs)
