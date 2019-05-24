# -*- coding: utf-8 -*-

"""Main module."""

import xmltodict


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
    pass


if __name__ == '__main__':
    main()
