# -*- coding: utf-8 -*-
"""
Admin config for short URLs.
"""
from django.contrib import admin

from shorty.models import ShortUrl


class ShortUrlAdmin(admin.ModelAdmin):
    """
    Admin config for the ShortUrl model.
    """
    list_display = ('url', 'clicks', 'short_code')
admin.site.register(ShortUrl, ShortUrlAdmin)
