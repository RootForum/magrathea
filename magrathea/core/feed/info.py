# -*- coding: utf-8 -*-
"""
    magrathea.core.feed.info
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""


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
