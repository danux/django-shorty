import re
import unicodedata
import urlparse
from datetime import datetime

from urllib import quote, unquote

from django.db import models

from couchdbkit.ext.django.schema import *

from shorty.base_62 import dehydrate, saturate


class ShortUrlManager(models.Manager):

    def get_by_code(self, code):
        return self.get(pk=saturate(code))

class ShortUrl(models.Model):

    url = models.CharField(max_length=255, unique=True, db_index=True)
    clicks = models.IntegerField(blank=True, null=True, default=0)

    objects = ShortUrlManager()

    @property
    def short_code(self):
        return dehydrate(self.pk)

    def save(self, *args, **kwargs):
        self.url_normalize()
        super(ShortUrl, self).save(*args, **kwargs)

    def url_normalize(self, charset='utf-8'):
        """
        Normalises the URL
        """
        def _clean(string):
            string = unicode(unquote(string), 'utf-8', 'replace')
            return unicodedata.normalize('NFC', string).encode('utf-8')

        default_port = {
            'ftp': 21,
            'telnet': 23,
            'http': 80,
            'gopher': 70,
            'news': 119,
            'nntp': 119,
            'prospero': 191,
            'https': 443,
            'snews': 563,
            'snntp': 563,
        }
        if isinstance(self.url, unicode):
            self.url = self.url.encode(charset, 'ignore')

        if self.url[0] not in ['/', '-'] and ':' not in self.url[:7]:
            self.url = 'http://' + self.url
            

        self.url = self.url.replace('#!', '?_escaped_fragment_=')

        scheme, auth, path, query, fragment = urlparse.urlsplit(self.url.strip())
        (userinfo, host, port) = re.search('([^@]*@)?([^:]*):?(.*)', auth).groups()

        scheme = scheme.lower()

        host = host.lower()
        if host and host[-1] == '.':
            host = host[:-1]
        host = host.decode(charset).encode('idna')

        path = quote(_clean(path), "~:/?#[]@!$&'()*+,;=")
        fragment = quote(_clean(fragment), "~")

        query = "&".join(["=".join([quote(_clean(t), "~:/?#[]@!$'()*+,;=") for t in q.split("=", 1)]) for q in query.split("&")])

        if scheme in ["", "http", "https", "ftp", "file"]:
            output = []
            for part in path.split('/'):
                if part == "":
                    if not output:
                        output.append(part)
                elif part == ".":
                    pass
                elif part == "..":
                    if len(output) > 1:
                        output.pop()
                else:
                    output.append(part)
            if part in ["", ".", ".."]:
                output.append("")
            path = '/'.join(output)

        if userinfo in ["@", ":@"]:
            userinfo = ""

        if path == "" and scheme in ["http", "https", "ftp", "file"]:
            path = "/"


        if port and scheme in default_port.keys():
            if port.isdigit():
                port = str(int(port))
                if int(port) == default_port[scheme]:
                    port = ''

        auth = (userinfo or "") + host
        if port:
            auth += ":" + port
        if self.url.endswith("#") and query == "" and fragment == "":
            path += "#"

        self.url = urlparse.urlunsplit((scheme, auth, path, query, fragment))


class Click(Document):
    date = DateTimeProperty(default=datetime.utcnow)

    def register(self, request):
        desired_keys = ('HTTP_HOST', 'HTTP_REFERER', 'HTTP_USER_AGENT', 'REMOTE_ADDR', )
        for key, value in request.META.iteritems():
            if key in desired_keys:
                setattr(self, key.lower(), value)

        self.session_key = request.session.session_key
