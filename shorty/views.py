from django.http import HttpResponseRedirect

from shorty.models import ShortUrl, Click


def convert(request, code):
    short_url = ShortUrl.objects.get_by_code(code)
    short_url.clicks += 1
    short_url.save()

    click = Click()
    click.register(request)
    click.save()

    return HttpResponseRedirect(short_url.url)