# -*- coding: utf-8 -*-

"""Main module."""

import xmltodict


def extract_feeds(opml):
    feeds = [i['@xmlUrl'] for i in opml['opml']['body']['outline']['outline']]

    return feeds


def get_entries(feed):
    entries = feed['feed']['entry']

    return entries


def main():
    pass


if __name__ == '__main__':
    main()
