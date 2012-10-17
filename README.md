standalone-url-shortener
========================

Importable app for Django projects to provide short URLs.

CREDITS
=======
Base 62 algorithm:  https://gist.github.com/778542
URL Normalisation:  http://code.google.com/p/url-normalize/

INSTALLATION
============

1. pip install git+https://github.com/danux/standalone-url-shortener.git#egg=shorty

2. Ensure the request is available to the context.

TEMPLATE_CONTEXT_PROCESSORS = (
    ...
    "django.core.context_processors.request",
)

3. Add shorty to available apps
INSTALLED_APPS = (
    ...
    'shorty',
)

4. Do a syncdb

5. Configure Django sites framework with correct FQDN

USAGE
=====

1. Add {% load shorty_tags %} to your template

2. Use {% short_url %} to display the short url on the page