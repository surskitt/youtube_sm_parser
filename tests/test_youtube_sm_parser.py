#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `youtube_sm_parser` package."""

import pytest

import os


from youtube_sm_parser import youtube_sm_parser


def mock_xml(fn):
    dir_name = os.path.dirname(os.path.realpath(__file__))
    full_fn = os.path.join(dir_name, fn)
    with open(full_fn) as f:
        return f.read()


@pytest.fixture
def subs_file():
    return mock_xml('subscription_manager.xml')


@pytest.fixture
def feed():
    return mock_xml('feed.xml')


@pytest.fixture
def entry1():
    return mock_xml('entry1.xml')


@pytest.fixture
def entry1():
    return mock_xml('entry2.xml')


def test_extract_feeds(subs_file):
    expected = ['test_chan_url', 'test_chan_url_2']
    parsed_urls = youtube_sm_parser.extract_feeds(subs_file)

    assert parsed_urls == expected


def test_get_entries(feed):
    pass


def test_entry_to_dict():
    pass
