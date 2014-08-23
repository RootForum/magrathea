# -*- coding: utf-8 -*-
"""
    magrathea.core.feed.entry
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import base64
import calendar
import time
from ...utils.convert import to_str, to_bytes


def get_entry_id(entry):
    """
    Retrieve the unique identifier of a :py:mod:`feedparser` entry object.
    Magrathea uses this internally for a identifying entry objects.

    :param entry: :py:mod:`feedparser` entry object
    """
    if hasattr(entry, 'id'):
        return base64.b64encode(to_bytes(entry.id))
    if hasattr(entry, 'link'):
        return base64.b64encode(to_bytes(entry.link))
    return None


class Entry(object):
    """
    Class representing a feed entry. To ease sorting of entries,
    each entry offers a sort key (``key`` property) constructed
    from its update date. If the feed does not provide the updated
    date, the publish date or the creation date are used.

    :param entry: A :py:mod:`feedparser` entry object
    """

    def __init__(self, entry):
        self._id = get_entry_id(entry)
        self._key = None
        self._updated = None
        self._expired = None
        self._link = None
        self._content = None
        self._description = None
        self._title = None
        self._author = None
        self._feed = None
        self._parse_entry(entry)

    def update(self, entry):
        """
        Update feed entry with new information.

        :param entry: A :py:mod:`feedparser` entry object
        """
        self._parse_entry(entry)

    def _parse_entry(self, entry):
        if hasattr(entry, 'updated_parsed'):
            self._updated = entry.updated_parsed
        if hasattr(entry, 'published_parsed') and not self._updated:
            self._updated = entry.published_parsed
        if hasattr(entry, 'created_parsed') and not self._updated:
            self._updated = entry.created_parsed
        if hasattr(entry, 'expired_parsed'):
            self._updated = entry.expired_parsed
        if hasattr(entry, 'link'):
            self._link = entry.link
        if hasattr(entry, 'content'):
            self._content = []
            for element in entry.content:
                self._content.append(element.value)
        if hasattr(entry, 'description'):
            self._description = entry.description
        if hasattr(entry, 'title'):
            self._title = entry.title
        if hasattr(entry, 'author'):
            self._author = entry.author
        if self._updated:
            self._key = time.strftime('%Y%m%d%H%M%S', self._updated)

    @property
    def id(self):
        """
        Unique identifier of the entry
        """
        return self._id

    @property
    def key(self):
        """
        Time-based sorting key
        """
        return self._key

    @property
    def body(self):
        """
        Content body of the entry
        """
        if self._content:
            # noinspection PyTypeChecker
            return " ".join(to_str(self._content))
        if self._description:
            return to_str(self._description)
        return ""

    @property
    def title(self):
        """
        Title of the entry
        """
        return to_str(self._title)

    @property
    def pubdate_gmt(self):
        """
        Date when the entry was last updated, published or otherwise changed in GMT
        """
        return self._updated

    @property
    def pubdate_local(self):
        """
        Date when the entry was last updated, published or otherwise changed converted to local time
        """
        return time.localtime(calendar.timegm(self._updated))

    @property
    def author(self):
        """
        Author of the entry
        """
        return to_str(self._author)

    @property
    def feed(self):
        """
        Feed the entry comes from.

        Available sub-attributes: :py:attr:`~magrathea.core.feed.feed.FeedInfo.author`,
        :py:attr:`~magrathea.core.feed.feed.FeedInfo.title`, :py:attr:`~magrathea.core.feed.feed.FeedInfo.uri` and
        :py:attr:`~magrathea.core.feed.feed.FeedInfo.type`.
        """
        return self._feed

    @feed.setter
    def feed(self, feed):
        from .feed import FeedInfo
        if isinstance(feed, FeedInfo):
            self._feed = feed

    def get_pubdate_gmt(self, format):
        """
        Get the :py:attr:`~magrathea.core.feed.entry.Entry.pubdate_gmt` (GMT) formatted via :py:func:`time.strftime`.

        :param str format: format string understood by :py:func:`time.strftime`
        """
        return time.strftime(format, self._updated)

    def get_pubdate_local(self, format):
        """
        Get the :py:attr:`~magrathea.core.feed.entry.Entry.pubdate_local` (local) formatted via
        :py:func:`time.strftime`.

        :param str format: format string understood by :py:func:`time.strftime`
        """
        return time.strftime(format, time.localtime(calendar.timegm(self._updated)))
