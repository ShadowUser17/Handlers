#!/usr/bin/env python3
from re import compile as re_compile
from urllib import parse as urllib
from html import parser as html
from os import path as filepath
from urllib import request


class Parser(html.HTMLParser):
    url_base = ''
    url_list = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == 'a':
            attrs = dict(attrs)
            item = attrs.get('href')

            if item:
                self.url_list.append(urllib.urljoin(self.url_base, item))


def get_url_data(url: str) -> list:
    with request.urlopen(url) as req:
        parser = Parser()
        parser.url_base = url
        parser.feed(req.read().decode())
        return parser.url_list.copy()


if __name__ == '__main__':
    url_regex = re_compile('^.*-(\d+)\/$')
    url_base = 'https://cloud.debian.org/images/cloud/bullseye/daily/'

    url_list = get_url_data(url_base)
    url_list = list(filter(lambda it: url_regex.match(it), url_list))

    if url_list:
        url_regex = re_compile('.*-(nocloud-amd64)-.*\.qcow2$')
        url_base = urllib.urlparse(url_list[-1])
        url_base = url_base.geturl()

        url_list = url_list = get_url_data(url_base)
        url_list = list(filter(lambda it: url_regex.match(it), url_list))

        if url_list:
            url = urllib.urlparse(url_list[-1])
            filename = filepath.basename(url.path)

            if not filepath.exists(filename):
                print('Start download: {}'.format(filename))
                (filename, _) = request.urlretrieve(url.geturl(), filename)

            else:
                print('File is exist: {}'.format(filename))
