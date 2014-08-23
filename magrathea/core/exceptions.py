# -*- coding: utf-8 -*-
"""
    magrathea.core.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from ..utils.dynamic import Dynamic


class MagratheaError(Dynamic, Exception):
    """
    Basic Magrathea Exception class

    :param list args:   list of positional arguments, will be ignored
    :param dict kwargs: keyword arguments, will be converted into Exception properties
    """

    def __init__(self, *args, **kwargs):
        super(MagratheaError, self).__init__(*args, **kwargs)


# Feed Exceptions

class FeedError(MagratheaError):
    """
    Exception class template for feed exceptions

    :param list args:   list of positional arguments, will be ignored
    :param dict kwargs: keyword arguments, will be converted into Exception properties
    """

    def __init__(self, *args, **kwargs):
        self._uri = ''
        self._href = ''
        self._title = ''
        self._type = ''
        super(FeedError, self).__init__(*args, **kwargs)


class FeedGoneError(FeedError):
    """
    Feed Gone Error

    This exception is raised when a feed has gone permanently.
    """
    def __str__(self):
        if self._uri:
            return "The feed at {uri} has permanently gone. Consider removing it from your configuration.".format(
                uri=self._uri
            )
        else:
            return "A feed has permanently gone (no details available)."


class FeedMovedError(FeedError):
    """
    Feed Moved Error

    This exception is raised when a feed has been moved permanently.
    """
    def __str__(self):
        if self._uri and self._href:
            return "The feed at {uri} has permanently moved to {href}. Consider updating your configuration.".format(
                uri=self._uri,
                href=self._href
            )
        elif self._uri and not self._href:
            return "The feed at {uri} has permanently moved to an unknown location.".format(uri=self._uri)
        elif not self._uri and self._href:
            return "An unknown feed has permanently moved to {href}.".format(href=self._href)
        else:
            return "A feed has permanently moved (no details available)."
