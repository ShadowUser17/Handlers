#!/usr/bin/env python3
from urllib import parse as urllib
from urllib import request
from html import parser as html
from os import path as filepath


class Parser(html.HTMLParser):
    url_base = ''
    url_list = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == 'a':
            attrs = dict(attrs)

            if (attrs.get('class', '') == 'download downloadBox') and attrs.get('href'):
                self.url_list.append(urllib.urljoin(self.url_base, attrs.get('href')))

    #def handle_data(self, data: str) -> None: pass
    #def handle_endtag(self, tag: str) -> None: pass


if __name__ == "__main__":
    url_base = 'https://golang.org/dl/'
    url_list = None

    with request.urlopen(url_base) as req:
        print('Get urls from: {}'.format(url_base))
        parser = Parser()
        parser.url_base = url_base
        parser.feed(req.read().decode())
        url_list = parser.url_list.copy()

    url = list(filter(lambda it: it.endswith('linux-amd64.tar.gz'), url_list))

    if url:
        url = urllib.urlparse(url[0])
        filename = filepath.basename(url.path)

        if not filepath.exists(filename):
            print('Start download: {}'.format(filename))
            (filename, headers) = request.urlretrieve(url.geturl(), filename)

        else:
            print('File is exist: {}'.format(filename))
