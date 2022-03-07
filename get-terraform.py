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

            if attrs.get('href'):
                url_item = attrs.get('href')

                if url_item.startswith('/'):
                    url_item = list(filter(None, url_item.split('/')))
                    sub_item = '{version}/terraform_{version}_linux_amd64.zip'.format(version=url_item[1])
                    url_item = urllib.urljoin(self.url_base, sub_item)
                    self.url_list.append(url_item)


if __name__ == '__main__':
    url_base = 'https://releases.hashicorp.com/terraform/'
    url_list = None

    with request.urlopen(url_base) as req:
        print('Get urls from: {}'.format(url_base))
        parser = Parser()
        parser.url_base = url_base
        parser.feed(req.read().decode())
        url_list = parser.url_list.copy()

    url_list = list(filter(lambda it: it.endswith('.zip'), url_list))

    if url_list:
        url = urllib.urlparse(url_list[0])
        filename = filepath.basename(url.path)

        if not filepath.exists(filename):
            print('Start download: {}'.format(filename))
            (filename, _) = request.urlretrieve(url.geturl(), filename)

        else:
            print('File is exist: {}'.format(filename))
