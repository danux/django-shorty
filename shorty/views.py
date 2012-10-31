from django.conf import settings
from django.http import HttpResponseRedirect

from shorty.models import ShortUrl, Click


def convert(request, code):
    short_url = ShortUrl.objects.get_by_code(code)
    short_url.clicks += 1
    short_url.save()

    if settings.ENABLE_CLICK_TRACKING:
        click = Click()
        click.register(request)
        click.code = code
        click.url = short_url.url
        click.unique_id = short_url.unique_id
        click.pk = short_url.pk
        click.save()

    return HttpResponseRedirect(short_url.url)