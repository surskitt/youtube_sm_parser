#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `youtube_sm_parser` package."""

import pytest

import io


from youtube_sm_parser import youtube_sm_parser


@pytest.fixture
def subs_file():
    subs_file = '''<?xml version="1.0"?>
    <opml version="1.1">
      <body>
        <outline text="YouTube Subscriptions" title="YouTube Subscriptions">
          <outline text="test" title="test" type="rss" xmlUrl="test_chan_url"/>
        </outline>
      </body>
    </opml>
    '''

    return io.StringIO(subs_file)


def test_parse_subs_file(subs_file):
    expected = ['test_chan_url']
    parsed_urls = youtube_sm_parser.parse_subs_file(subs_file)

    assert parsed_urls == expected
