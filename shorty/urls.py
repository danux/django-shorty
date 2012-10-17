from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<code>\d)$', 'shorty.views.convert', name='converter'),
)