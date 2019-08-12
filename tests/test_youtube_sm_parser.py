#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `youtube_sm_parser` package."""

import pytest
import unittest.mock
import deepdiff
import collections

import os
import xmltodict
import json


from youtube_sm_parser import youtube_sm_parser


def rel_fn(fn):
    dir_name = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_name, fn)


def mock_xml(fn):
    with open(rel_fn(fn)) as f:
        return xmltodict.parse(f.read())


def mock_xml_raw(fn):
    with open(rel_fn(fn)) as f:
        return f.read()


def mock_json(fn):
    with open(rel_fn(fn)) as f:
        return json.load(f, object_pairs_hook=collections.OrderedDict)


@pytest.fixture
def subs_file():
    return mock_xml('subscription_manager.xml')


@pytest.fixture
def feed():
    return mock_xml('feed.xml')


@pytest.fixture
def feed_raw():
    return mock_xml_raw('feed.xml')


@pytest.fixture
def entry_dict():
    return {
        'id': 'id',
        'title': 'video title',
        'link': 'video_url',
        'uploader': 'author name',
        'published': '2019-05-14T11:00:01+00:00',
        'thumbnail': 'thumb_url'
    }


def test_extract_feeds(subs_file):
    expected = ['test_chan_url', 'test_chan_url_2']
    parsed_urls = youtube_sm_parser.extract_feeds(subs_file)

    assert parsed_urls == expected


def test_get_entries(feed):
    expected = [mock_json(i) for i in ['entry1.json', 'entry2.json']]

    entries = youtube_sm_parser.get_entries(feed)

    assert deepdiff.DeepDiff(entries, expected) == {}


def test_get_entries_empty():
    expected = []
    entries = youtube_sm_parser.get_entries({'feed': {}})

    assert entries == expected


def test_entry_to_dict(entry_dict):
    entry = mock_json('entry1.json')
    expected = youtube_sm_parser.entry_to_dict(entry)

    assert deepdiff.DeepDiff(entry_dict, expected) == {}


def test_format_dict(entry_dict):
    format_string = '{title},{link}'
    expected = 'video title,video_url'
    formatted = youtube_sm_parser.format_dict(entry_dict, format_string)

    assert formatted == expected


def test_feed_to_dicts(feed_raw, entry_dict):
    class r():
        content = feed_raw

    entry_dicts = youtube_sm_parser.feed_to_dicts(r).data

    assert entry_dicts[0] == entry_dict


@pytest.mark.parametrize('f', ['json', 'lines', 'yaml'])
def test_parse_args_format(f):
    args = youtube_sm_parser.parse_args(['--format', f])
    assert args.format == f


def test_invalid_format():
    with pytest.raises(SystemExit):
        args = youtube_sm_parser.parse_args('--format invalid'.split())


def test_line_format_valid():
    args = youtube_sm_parser.parse_args('-l {title}'.split())
    assert args.line_format == '{title}'


def test_line_format_invalid():
    with pytest.raises(SystemExit):
        args = youtube_sm_parser.parse_args('-l {invalid}'.split())


@unittest.mock.patch('youtube_sm_parser.youtube_sm_parser.FuturesSession')
def test_get_subscriptions(mock_fs, feed):
    mock_fs.return_value.get.return_value.content = feed

    subs = youtube_sm_parser.get_subscriptions(['blah'], 10)


@pytest.mark.parametrize('out_format, expected, line_format', [
    ['json', '[\n    {\n        "a": "b"\n    }\n]', None],
    ['lines', 'b', '{a}'],
    ['yaml', '- a: b\n', None]
])
def test_get_output(out_format, expected, line_format):
    entries = [{'a': 'b'}]

    output = youtube_sm_parser.get_output(entries, out_format, line_format)
    assert expected == output
