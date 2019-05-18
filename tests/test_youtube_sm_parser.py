#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `youtube_sm_parser` package."""

import pytest
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


def mock_json(fn):
    with open(rel_fn(fn)) as f:
        return json.load(f, object_pairs_hook=collections.OrderedDict)


@pytest.fixture
def subs_file():
    return mock_xml('subscription_manager.xml')


@pytest.fixture
def feed():
    return mock_xml('feed.xml')


#  @pytest.fixture
#  def entry1():
#      return mock_json('entry1.json')


def test_extract_feeds(subs_file):
    expected = ['test_chan_url', 'test_chan_url_2']
    parsed_urls = youtube_sm_parser.extract_feeds(subs_file)

    assert parsed_urls == expected


def test_get_entries(feed):
    expected = [mock_json(i) for i in ['entry1.json', 'entry2.json']]

    entries = youtube_sm_parser.get_entries(feed)

    assert deepdiff.DeepDiff(expected, entries) == {}


def test_entry_to_dict():
    pass
