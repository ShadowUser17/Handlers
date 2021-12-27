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
            item = attrs.get('href')

            if item:
                self.url_list.append(urllib.urljoin(self.url_base, item))


if __name__ == '__main__':
    url_base = 'http://archlinux.astra.in.ua/iso/latest/'
    url_list = None

    with request.urlopen(url_base) as req:
        parser = Parser()
        parser.url_base = url_base
        parser.feed(req.read().decode())
        url_list = parser.url_list.copy()

    url_list = list(filter(lambda it: it.endswith('x86_64.iso'), url_list))

    if url_list:
        url = urllib.urlparse(url_list[0])
        filename = filepath.basename(url.path)

        if not filepath.exists(filename):
            print('Start download: {}'.format(filename))
            (filename, _) = request.urlretrieve(url.geturl(), filename)

        else:
            print('File is exist: {}'.format(filename))
