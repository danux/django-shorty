from django.core.urlresolvers import reverse

from shorty.models import ShortUrl

def create_short_url(sender, **kwargs):
    instance = kwargs['instance']
    short_url = ShortUrl.objects.get_or_create(url=instance.get_absolute_url())

def get_short_url(url):
    return reverse('shorty:converter', args=(ShortUrl.objects.get(url=url).short_code,) )