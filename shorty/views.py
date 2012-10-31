from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from shorty.models import ShortUrl, Click


def convert(request, code):
    try:
        short_url = ShortUrl.objects.get_by_code(code)
    except ShortUrl.DoesNotExist:
        Http404()

    safe_mode = request.GET.get('safe_mode', False)

    short_url.clicks += 1
    short_url.save()

    if settings.ENABLE_CLICK_TRACKING:
        click = Click()
        click.register(request)
        click.code = code
        click.url = short_url.url
        click.unique_id = short_url.unique_id
        click.pk = short_url.pk
        if safe_mode:
            click.safe_mode = True
        click.save()

    if safe_mode:
        return render_to_response("shorty/safe-mode.html", {'short_url': short_url})
    else:
        return HttpResponseRedirect(short_url.url)