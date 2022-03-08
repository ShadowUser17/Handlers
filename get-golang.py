#!/usr/bin/env python3
from urllib import parse as urllib
from urllib import request
from html import parser as html
from os import path as filepath
from sys import platform


class Parser(html.HTMLParser):
    url_base = ''
    url_list = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == 'a':
            attrs = dict(attrs)

            if (attrs.get('class', '') == 'download downloadBox') and attrs.get('href'):
                self.url_list.append(urllib.urljoin(self.url_base, attrs.get('href')))


if __name__ == '__main__':
    url_base = 'https://go.dev/dl/'
    url_list = None

    with request.urlopen(url_base) as req:
        print('Get urls from: {}'.format(url_base))
        parser = Parser()
        parser.url_base = url_base
        parser.feed(req.read().decode())
        url_list = parser.url_list.copy()

    if platform.startswith('darwin'):
        url_list = list(filter(lambda it: it.endswith('darwin-amd64.pkg'), url_list))

    elif platform.startswith('cygwin'):
        url_list = list(filter(lambda it: it.endswith('windows-amd64.msi'), url_list))

    else:
        url_list = list(filter(lambda it: it.endswith('linux-amd64.tar.gz'), url_list))

    if url_list:
        url = urllib.urlparse(url_list[0])
        filename = filepath.basename(url.path)

        if not filepath.exists(filename):
            print('Start download: {}'.format(filename))
            (filename, _) = request.urlretrieve(url.geturl(), filename)

        else:
            print('File is exist: {}'.format(filename))
