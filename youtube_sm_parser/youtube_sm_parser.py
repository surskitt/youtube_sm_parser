# -*- coding: utf-8 -*-

"""Main module."""

import xml.etree.ElementTree


def extract_feeds(subs_file):
    x = xml.etree.ElementTree.fromstring(subs_file)
    feeds = [i.get('xmlUrl') for i in x.findall('body/outline/outline')]

    return feeds


def main():
    pass


if __name__ == '__main__':
    main()
