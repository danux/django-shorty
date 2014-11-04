# -*- coding: utf-8 -*-
"""
Template tag for creating and displaying a page's short URL.
"""
from django import template
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from shorty.models import ShortUrl


register = template.Library()


def short_url(context):
    """
    Template tag that will create and return a short URL for the current page.
    :type context: {}
    :return: unicode
    """
    try:
        request = context['request']
    except KeyError:
        raise Exception(
            'Request not available to URL shortener, ensure context processor: '
            'django.core.context_processors.request is available.'
        )
    
    try:
        if settings.SHORT_URL_FULL_URL:
            path = request.get_full_path()
        else:
            path = request.path
    except AttributeError:
        path = request.path

    url, created = ShortUrl.objects.get_or_create(url=path)
    short_url_string = reverse('shorty:converter', args=(url.short_code,))

    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'

    fqdn = get_current_site(request).domain
    return '%s%s%s' % (protocol, fqdn, short_url_string)
register.simple_tag(takes_context=True)(short_url)
