# -*- coding: utf-8 -*-
"""
    magrathea.core.result
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from ..utils.timer import counter


class Result(object):
    """
    Class representing the result of a planet operation.

    By default, a result object represents a succeeded operation
    without any further messages.
    """

    def __init__(self):
        self._status = True
        self._messages = {}

    def __bool__(self):
        """
        Override bool() operation result on result objects
        """
        return self._status

    @property
    def status(self):
        """
        Boolean indicating whether the operation succeeded or not
        """
        return self._status

    @property
    def messages(self):
        """
        List of message tuples in the order of occurrence. Each message
        is represented by a tuple (level, message), with both elements
        being strings.
        """
        msg = []
        for message in sorted(self._messages.keys()):
            msg.append((self._messages[message][0], self._messages[message][1]))
        return msg

    @property
    def messages_raw(self):
        """
        Raw message dictionary. This property should only be used for merging
        result objects.
        """
        return self._messages

    def fail(self, message=''):
        """
        Record that current operation failed

        :param str message: error message to be appended to messages list
        """
        self._status = False
        if message:
            self._messages[counter()] = ('error', message)

    def succeed(self, message=''):
        """
        Record that current operation succeeded

        :param str message: success message to be appended to messages list
        """
        self._status = True
        if message:
            self._messages[counter()] = ('debug', message)

    def warn(self, message=''):
        """
        Record a warning message

        :param str message: warning message to be appended to messages list
        """
        if message:
            self._messages[counter()] = ('warning', message)

    def merge(self, result):
        """
        Merge a result object into this result

        :param result: result object to be merged
        """
        self._status = self._status and result.status
        self._messages.update(result.messages_raw)
