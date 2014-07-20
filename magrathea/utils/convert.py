# -*- coding: utf-8 -*-
"""
    magrathea.utils.convert
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import sys
from ..conf import get_conf


def to_bytes(value):
    """
    Convert any value into a byte sequence.

    :param value: The value to be converted
    :return: Byte sequence
    """
    if sys.version_info < (3, 0, 0):
        if isinstance(value, unicode):
            return str(bytearray(source=value, encoding=get_conf('DEFAULT_CHARSET'), errors='replace'))
        elif isinstance(value, bytearray):
            return str(value)
        elif value is None:
            return b''
        else:
            return str(bytearray(source=str(value), encoding=get_conf('DEFAULT_CHARSET'), errors='replace'))
    else:
        if isinstance(value, str):
            # noinspection PyArgumentList
            return bytes(source=value, encoding=get_conf('DEFAULT_CHARSET'), errors='replace')
        elif isinstance(value, bytearray):
            return bytes(value)
        elif isinstance(value, bytes):
            return value
        elif value is None:
            return b''
        else:
            # noinspection PyArgumentList
            return bytes(source=str(value), encoding=get_conf('DEFAULT_CHARSET'), errors='replace')


def to_str(value):
    """
    Convert any value into a unicode string.

    :param value: The value to be converted
    :return: Resulting string
    """
    if sys.version_info < (3, 0, 0):
        if isinstance(value, str):
            return unicode(value, encoding=get_conf('DEFAULT_CHARSET'), errors='replace')
        elif isinstance(value, bytearray):
            return unicode(str(value), encoding=get_conf('DEFAULT_CHARSET'), errors='replace')
        elif value is None:
            return u''
        else:
            return unicode(str(value), encoding=get_conf('DEFAULT_CHARSET'), errors='replace')
    else:
        if isinstance(value, bytes) or isinstance(value, bytearray):
            return value.decode(encoding=get_conf('DEFAULT_CHARSET'), errors='replace')
        elif value is None:
            return ''
        else:
            return str(value)
