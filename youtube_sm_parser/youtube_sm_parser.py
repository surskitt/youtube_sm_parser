# -*- coding: utf-8 -*-

"""Main module."""


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


def main():
    pass


if __name__ == '__main__':
    main()
