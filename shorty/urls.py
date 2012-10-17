from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<code>[\d\w])$', 'shorty.views.convert', name='converter'),
)