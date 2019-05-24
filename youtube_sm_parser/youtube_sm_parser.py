# -*- coding: utf-8 -*-

"""Main module."""

import sys
import xmltodict
from requests_futures.sessions import FuturesSession


def extract_feeds(opml):
    feeds = [i['@xmlUrl'] for i in opml['opml']['body']['outline']['outline']]

    return feeds


def get_entries(feed):
    entries = feed['feed'].get('entry', [])

    return entries


def entry_to_dict(entry):
    entry_dict = {
        'id': entry['yt:videoId'],
        'title': entry['title'],
        'link': entry['link']['@href'],
        'uploader': entry['author']['name'],
        'published': entry['published'],
        'thumbnail': entry['media:group']['media:thumbnail']['@url']
    }
    return entry_dict


def format_dict(d, format_string):
    return format_string.format(**d)


def feed_to_dicts(r, *args, **kwargs):
    feed_dict = xmltodict.parse(r.content)
    entries = get_entries(feed_dict)
    entry_dicts = [entry_to_dict(e) for e in entries]
    r.data = entry_dicts

    return r


def main():
    opml_fn = sys.argv[1]
    with open(opml_fn) as f:
        opml_dict = xmltodict.parse(f.read())
    feeds = extract_feeds(opml_dict)

    session = FuturesSession(max_workers=50)
    futures = [session.get(f, hooks={'response': feed_to_dicts})
               for f in feeds]
    entry_lists = [f.result().data for f in futures]
    entries = [i for s in entry_lists for i in s]


if __name__ == '__main__':
    main()
