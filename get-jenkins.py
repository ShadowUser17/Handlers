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

            if (attrs.get('class', '') == 'list-group-item list-group-item-action') and attrs.get('href'):
                self.url_list.append(urllib.urljoin(self.url_base, attrs.get('href')))


if __name__ == '__main__':
    url_base = 'https://www.jenkins.io/download/'
    url_list = None

    with request.urlopen(url_base) as req:
        print('Get urls from: {}'.format(url_base))
        parser = Parser()
        parser.url_base = url_base
        parser.feed(req.read().decode())
        url_list = parser.url_list.copy()

    url_list = list(filter(lambda it: it.endswith('jenkins.war'), url_list))

    if url_list:
        url = urllib.urlparse(url_list[0])
        version = filepath.dirname(url.path)
        version = filepath.basename(version)

        filename = filepath.basename(url.path)
        filename = filename.split('.')
        filename = '{}-{}.{}'.format(filename[0], version, filename[1])

        if not filepath.exists(filename):
            print('Start download: {}'.format(filename))
            (filename, _) = request.urlretrieve(url.geturl(), filename)

        else:
            print('File is exist: {}'.format(filename))
