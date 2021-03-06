# django-shorty

[![Build Status](https://travis-ci.org/danux/django-shorty.svg)](https://travis-ci.org/danux/django-shorty)
[![Coverage Status](https://coveralls.io/repos/danux/django-shorty/badge.svg?branch=master&service=github)](https://coveralls.io/github/danux/django-shorty?branch=master)

Importable app for Django projects to provide short URLs.

URL generation is based on a Bijective function i.e. it's based around base 62 encoding of the URL's PK

## Credits

Base 62 algorithm:  https://gist.github.com/778542

## Installation

1. pip install git+https://github.com/danux/django-shorty.git#egg=shorty

2. Ensure the request is available to the context.
```python
TEMPLATE_CONTEXT_PROCESSORS = (
    ...
    "django.core.context_processors.request",
)
```

3. Add shorty to available apps
```python
INSTALLED_APPS = (
    ...
    'shorty',
)
```

4. Add Urls. Either place this at the end of your urls for domain.com/CodE
```python
url(r'^', include('shorty.urls', namespace='shorty')),
```
or, place it anywhere and append something else to the request, i.e. domain.com/s/CodE
```python
url(r'^s/', include('shorty.urls', namespace='shorty')),
```

5. Do a syncdb

6. Configure Django sites framework with correct FQDN

## Usage

1. Add {% load shorty_tags %} to your template

2. Use {% short_url %} to display the short url on the page

## Extras

By default, only the normal path will be used. If you want to include the query string add this to your settings
```python
settings.SHORT_URL_FULL_URL = True
```

Be warned, this means every request with a query string will be given a short URL and could be open to abuse. This is disabled by default.
