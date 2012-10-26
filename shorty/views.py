from django.http import HttpResponseRedirect

from shorty.models import ShortUrl


def convert(request, code):
    short_url = ShortUrl.objects.get_by_code(code)
    short_url.clicks += 1
    short_url.save()
    return HttpResponseRedirect(short_url.url)