from django.contrib import admin

from shorty.models import ShortUrl


class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'clicks', 'short_code')

admin.site.register(ShortUrl, ShortUrlAdmin)
