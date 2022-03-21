#!/usr/bin/env python3
from os import path as filepath
from html import parser as html
from urllib import request
from sys import platform


class Parser(html.HTMLParser):
    url_stat = False
    url_temp = None
    url_list = []
    sys_name = ''

    def __init__(self) -> None:
        html.HTMLParser.__init__(self)
        self.get_platform()

    def get_platform(self):
        if platform.startswith('cygwin'):
            self.sys_name = 'windows-x64-installer.exe'

        else:
            self.sys_name = 'linux-x64-installer.run'

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == 'a':
            attrs = dict(attrs)

            if attrs.get('href'):
                url_item = attrs.get('href')

                if url_item.startswith('https'):
                    self.url_temp = url_item
                    self.url_stat = True

    def handle_data(self, data: str) -> None:
        if self.url_stat and data.endswith(self.sys_name):
            self.url_list.append((self.url_temp, data))
            self.url_stat = False


if __name__ == '__main__':
    url_site = 'https://github.com/rapid7/metasploit-framework/wiki/Downloads-by-Version'
    url_list = None

    with request.urlopen(url_site) as req:
        print('Get urls from: {}'.format(url_site))
        parser = Parser()
        parser.feed(req.read().decode())
        url_list = parser.url_list.copy()

    if url_list:
        url = url_list[0][0]
        filename = url_list[0][1]

        if not filepath.exists(filename):
            print('Start download: {}'.format(filename))
            (filename, _) = request.urlretrieve(url, filename)

        else:
            print('File is exist: {}'.format(filename))
