# -*- coding: utf-8 -*-

"""Main module."""

import os
import sys
import xmltodict
import argparse
import json
import yaml

from requests_futures.sessions import FuturesSession


def line_validator(line_format):
    line_keys = ['id', 'title', 'link', 'uploader', 'published', 'thumbnail']
    try:
        line_format.format(**{k: 'test' for k in line_keys})
    except KeyError:
        error_msg = f'{line_format} is not a valid format'
        raise argparse.ArgumentTypeError(error_msg)
    return line_format


def parse_args(args):
    desc = 'Output subscriptions using subscription_manager file'
    parser = argparse.ArgumentParser(description=desc)

    format_choices = ['json', 'lines', 'yaml']
    parser.add_argument('-f', '--format', choices=format_choices,
                        default='lines')

    parser.add_argument('-l', '--line_format', default='{title},{link}',
                        type=line_validator)

    default_input_fn = '~/.config/youtube_sm_parser/subscription_manager'
    parser.add_argument('-i', '--input', default=default_input_fn)

    parser.add_argument('-w', '--workers', default=10, type=int)

    return parser.parse_args(args)


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
    args = parse_args(sys.argv[1:])

    with open(os.path.expanduser(args.input)) as f:
        opml_dict = xmltodict.parse(f.read())
    feeds = extract_feeds(opml_dict)

    session = FuturesSession(max_workers=args.workers)
    futures = [session.get(f, hooks={'response': feed_to_dicts})
               for f in feeds]
    entry_lists = [f.result().data for f in futures]
    entries = sorted([i for s in entry_lists for i in s],
                     key=lambda x: x['published'], reverse=True)

    if args.format == 'json':
        output = json.dumps(entries, indent=4)
    elif args.format == 'lines':
        output = '\n'.join(format_dict(line, args.line_format)
                           for line in entries)
    elif args.format == 'yaml':
        output = yaml.dump(entries)

    print(output)
