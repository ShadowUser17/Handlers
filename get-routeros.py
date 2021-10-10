#!/usr/bin/env python3
from urllib import parse as urllib
from urllib import request
from html import parser as html
from os import path as filepath


class Parser(html.HTMLParser):
    url_list = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == 'a':
            attrs = dict(attrs)

            if attrs.get('href'):
                url = urllib.urlparse(attrs.get('href', ''))

                if url.scheme == 'https' and url.netloc.startswith('download'):
                    filename = filepath.basename(url.path)

                    if filename.startswith('routeros-mipsbe'):
                        self.url_list.append(url.geturl())


if __name__ == '__main__':
    url_base = 'https://mikrotik.com/download'
    url_list = None

    with request.urlopen(url_base) as req:
        parser = Parser()
        parser.feed(req.read().decode())
        url_list = parser.url_list.copy()

    for item in url_list[:2]:
        item = urllib.urlparse(item)
        filename = filepath.basename(item.path)

        if not filepath.exists(filename):
            print('Start download: {}'.format(filename))
            (filename, _) = request.urlretrieve(item.geturl(), filename)

        else:
            print('File is exist: {}'.format(filename))
