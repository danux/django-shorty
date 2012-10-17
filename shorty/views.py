from django.http import HttpResponseRedirect

from shorty.base_62 import saturate, dehydrate
from shorty.models import ShortUrl

def convert(request, code):
    short_url = ShortUrl.objects.get(pk=saturate(code))
    short_url.clicks += 1
    short_url.save()
    return HttpResponseRedirect(short_url.url)