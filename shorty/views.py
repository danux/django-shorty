# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from shorty.models import ShortUrl


def convert(request, code):
    """
    View that converts codes in to URLs. If safemode is enable the user must confirm the redirect, otherwise
    the redirect is automatic.

    :type request: HttpRequest
    :type code: unicode
    :return: HttpResponse
    """
    try:
        short_url = ShortUrl.objects.get_by_code(code)
    except ShortUrl.DoesNotExist:
        raise Http404()

    safe_mode = request.GET.get('safe_mode', False)

    short_url.clicks += 1
    short_url.save()

    if safe_mode:
        return render_to_response("shorty/safe-mode.html", {'short_url': short_url}, RequestContext(request))
    else:
        return HttpResponseRedirect(short_url.url)
