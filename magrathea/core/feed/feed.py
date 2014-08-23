# -*- coding: utf-8 -*-
"""
    magrathea.core.feed.feed
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import base64
import feedparser
from ..exceptions import FeedGoneError, FeedMovedError
from ...utils.convert import to_bytes, to_str
from .entry import Entry


class FeedInfo(object):
    """
    A simple namespace object for passing information to an entry
    """

    def __init__(self, author, title, uri, version):
        self._author = author
        self._title = title
        self._uri = uri
        self._type = version

    @property
    def author(self):
        """Author of the feed"""
        return self._author

    @property
    def title(self):
        """Title of the feed"""
        return self._title

    @property
    def uri(self):
        """URI of the feed"""
        return self._uri

    @property
    def type(self):
        """Type of the feed"""
        return self._type


class Feed(object):
    """
    Class representing a feed. At least the URI or Key argument is required.
    If title and author are not specified, they will be guessed at the
    feed's first update.

    :param str uri: URI of the feed this object shall represent
    :param str key: Base64 encoded URI of the feed this object shall represent
    :param str title: Title to be tied with this feed
    :param str author: Author to be tied with this feed
    """

    def __init__(self, uri=None, key=None, title=None, author=None):
        self._author = author or None
        self._author_flag = True if author else False
        self._key = key or None
        self._title = title or None
        self._title_flag = True if title else False
        self._uri = uri or None
        self._entries = []
        self._etag = None
        self._modified = None
        self._type = None
        if uri and not key:
            self._key = base64.b64encode(to_bytes(uri))
        if key and not uri:
            self._uri = base64.b64decode(to_bytes(key))
        self._title = None
        self._author = None
        self._update_flag = False
        self._gone = False

    @property
    def author(self):
        """
        Author of the feed.
        """
        if not self._update_flag:
            self.update()
        return self._author

    @property
    def key(self):
        """
        Byte sequence identifying the feed. Granted to contain only printable characters.
        Thus, this key can safely be used as :py:mod:`shelve` database key.
        """
        return self._key

    @property
    def title(self):
        """
        Title of the feed.
        """
        if not self._update_flag:
            self.update()
        return self._title

    @property
    def uri(self):
        """
        URI of the feed.
        """
        return self._uri

    @property
    def entries_unordered(self):
        """
        List of entries without specific order
        """
        if not self._update_flag:
            self.update()
        return self._entries

    @property
    def entries_asc(self):
        """
        List of entries in ascending order (by their publishing date)
        """
        if not self._update_flag:
            self.update()
        return sorted(self._entries, key=lambda entry: entry.key, reverse=False)

    @property
    def entries_desc(self):
        """
        List of entries in descending order (by their publishing date)
        """
        if not self._update_flag:
            self.update()
        return sorted(self._entries, key=lambda entry: entry.key, reverse=True)

    @property
    def etag(self):
        """
        Etag provided by the feed's web server
        """
        if not self._update_flag:
            self.update()
        return self._etag

    @property
    def modified(self):
        """
        Modified header provided by the feed's web server
        """
        if not self._update_flag:
            self.update()
        return self._modified

    @property
    def type(self):
        """
        String identifying the type of the feed
        """
        if not self._update_flag:
            self.update()
        return self._type

    def update(self):
        """
        Update this feed object.

        This method is called implicitly when an attribute is accessed for the
        first time that requires the feed to be updated at least once.

        If the feed represented by this instance has gone permanently, no
        update will be performed. Instead, a
        :py:exc:`~magrathea.core.exception.FeedGoneError` is raised.

        If the feed represented by this instance has moved permanently, the
        update will be performed. In addition, a
        :py:exc:`~magrathea.core.exception.FeedMovedError` is raised.
        """
        if not self._uri:
            return
        if self._gone:
            raise FeedGoneError(uri=self._uri)
        result = feedparser.parse(self._uri, etag=self._etag, modified=self._modified)
        if hasattr(result, 'etag') and result.etag:
            self._etag = result.etag
        if hasattr(result, 'modified') and result.modified:
            self._modified = result.modified
        if hasattr(result, 'version') and result.version:
            self._type = result.version
        else:
            self._type = 'unknown'
        if hasattr(result, 'status') and result.status not in (304, 410):
            self._update(result)
        if hasattr(result, 'status') and result.status == 410:
            self._gone = True
            raise FeedGoneError(uri=self._uri)
        self._update_flag = True
        if hasattr(result, 'status') and result.status == 301:
            if hasattr(result, 'href'):
                raise FeedMovedError(href=result.href, uri=self._uri)
            else:
                raise FeedMovedError(uri=self._uri)

    def _update(self, parser):
        """
        Update the feed from a :py:mod:`feedparser` result object.

        This method is intended to be called by :py:meth:`~magrathea.core.feed.feed.Feed.update`.
        It is strongly advised to never call it directly.

        :param parser: A :py:mod:`feedparser` result object
        """
        self._update_entries(parser.entries)
        if not self._title_flag:
            if 'title' in parser.feed:
                self._title = to_str(parser.feed.title)
        if not self._author_flag:
            if 'author' in parser.feed:
                self._author = to_str(parser.feed.author)
            else:
                recent_entry = self._get_entry_most_recent()
                if recent_entry:
                    self._author = recent_entry.author
        for entry in self._entries:
            entry.feed = FeedInfo(self._author, self._title, self._uri, self._type)

    def _update_entries(self, entries):
        """
        Update the feed's entries from a :py:mod:`feedparser` entries list.

        :param list entries: A list of :py:mod:`feedparser` entry objects
        """
        for entry in entries:
            if hasattr(entry, 'id'):
                existing = self._get_entry_by_id(entry.id)
                if existing:
                    index = self._entries.index(existing)
                    self._entries[index].update(entry)
                else:
                    self._entries.append(Entry(entry))

    def _get_entry_most_recent(self):
        """
        Convenience method for retrieving the most recent entry.

        :return: a :py:class:`~magrathea.core.feed.entry.Entry` instance or ``None``.
        """
        try:
            return sorted(self._entries, key=lambda entry: entry.key, reverse=True)[0]
        except IndexError:
            return None

    def _get_entry_by_id(self, entry_id):
        """
        Get an entry object by its id.

        :param str entry_id: the string identifying an entry object.
        :return: a :py:class:`~magrathea.core.feed.entry.Entry` instance or ``None``.
        """
        entries = self._get_entries_by_property('id', entry_id)
        if entries and len(entries) == 1:
            return entries[0]
        elif entries and len(entries) > 1:
            # try healing this issue
            for entry in entries[1:]:
                self._entries.remove(entry)
            return entries[0]
        else:
            return None

    def _get_entries_by_property(self, item, value):
        """
        Get a subset of entries, whose attribute ``item`` has the value ``value``.

        :param str item: name of the entry attribute to be used for selection
        :param value:    value of the attribute to be filtered
        :return:         list of :py:class:`~magrathea.core.feed.entry.Entry` instances
        """
        result = []
        for entry in self._entries:
            if hasattr(entry, item):
                if getattr(entry, item) == value:
                    result.append(entry)
        return result
