# -*- coding: utf-8 -*-
"""
    magrathea.utils.compat
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import io
import os
import stat
import sys
import errno
from .convert import to_str
from magrathea.conf import get_conf

try:
    from io import open as io_open
except ImportError:
    from _pyio import open as io_open

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
from collections import OrderedDict


def comp_makedirs(name, mode=0o777, exist_ok=False):
    """
    Compatibility wrapper for :py:func:`os.makedirs`. It behaves
    identically to the :py:func:`os.makedirs` implementation in
    Python >=3.4.1, i. e. it brings the ``exist_ok`` argument back to
    older Python versions.

    .. note::

       Just as the real implementation in Python >=3.4.1, ``exist_ok=True``
       will now also prevent an :py:exc:`OSError` being raised when the mode
       of the already existing directory differs from the to-be mode
       either submitted as argument or taken from the default value.

    :param name: directory to be created
    :param mode: mode to be used for directory creation
    :param exist_ok: If set to ``True``, do not raise :py:exc:`OSError` when the directory already exists.
    """
    if sys.version_info >= (3, 4, 1):
        # noinspection PyArgumentList
        os.makedirs(name, mode=mode, exist_ok=exist_ok)
    else:
        if os.path.exists(name) and exist_ok:
            return
        else:
            os.makedirs(name, mode=mode)


def comp_open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    """
    Compatibility wrapper for :py:func:`open`. This function makes more advanced
    options from Python 3 available for Python 2. Similar to the Python 3 implementation
    of :py:func:`open`, this function may act as :py:keyword:`with` statement context manager.

    Other than the original :py:func:`open` function in Python 2, this function does not
    return a legacy file object (``<type 'file'>``) when used on Python 2. Instead, as in
    Python 3, it returns an :py:mod:`io` wrapper object, depending on what kind of file has
    been opened (binary or text). For text files, this will most likely be something like
    ``<type '_io.TextIOWrapper'>``.

    .. note::

       In case no encoding is specified, the default encoding as defined by
       :py:data:`magrathea.conf.default.DEFAULT_CHARSET` will be used.

    :param file: file is either a string or bytes object giving the pathname or
                 an integer file descriptor of the file to be wrapped
    :param mode: specifies the mode in which the file is opened
    :param buffering: optional integer used to set the buffering policy
    :param encoding: name of the encoding used to decode or encode the file
    :param errors: optional string that specifies how encoding and decoding errors are to be handled
    :param newline: controls how universal newlines mode works
    :param closefd: if False and a file descriptor rather than a filename was given, the underlying
                    file descriptor will be kept open when the file is closed
    :param opener: custom opener
    :returns: a :py:term:`file object`
    """
    if not encoding:
        encoding = get_conf('DEFAULT_CHARSET')
    if sys.version_info < (3, 0, 0):
        fp = io_open(
            file,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd
        )
    else:
        fp = open(
            file,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener
        )
    return fp


# Black magic for getting the right config parser class...
if sys.version_info >= (3, 2, 0):
    CP = configparser.ConfigParser
else:
    CP = configparser.SafeConfigParser

DEFAULTSECT = configparser.DEFAULTSECT
_UNSET = getattr(configparser, '_UNSET', object())
_default_dict = getattr(configparser, '_default_dict', OrderedDict)


class CompConfigParser(CP, object):
    """
    Compatibility wrapper for :py:class:`configparser.ConfigParser` or
    :py:class:`configparser.SafeConfigParser` for Python versions before 3.2

    .. note::

       This implementation does not guarantee to provide the dictionary-like
       interface introduced with Python 3.2 (otherwise, this could easily end
       up being a complete rewrite of the configparser module).

       Therefore, it is highly recommended to not rely on this way of accessing
       the contents of this configuration parser. Instead, use
       :py:meth:`~configparser.ConfigParser.sections`,
       :py:meth:`~configparser.ConfigParser.options` and
       :py:meth:`~configparser.ConfigParser.items` methods.

    .. warning::

       Although the original implementation of :py:class:`configparser.SafeConfigParser`
       in Python versions prior to 3.2 used to be an old-style class, this implementation
       provides a new-style class, also for Python versions prior to 3.2. Keep this in
       mind when inheriting from this class!
    """

    def __init__(self, defaults=None, dict_type=_default_dict,
                 allow_no_value=False, delimiters=('=', ':'),
                 comment_prefixes=('#', ';'), inline_comment_prefixes=None,
                 strict=True, empty_lines_in_values=True,
                 default_section=DEFAULTSECT,
                 interpolation=_UNSET):
        if sys.version_info >= (3, 2, 0):
            super(CompConfigParser, self).__init__(
                defaults=defaults,
                dict_type=dict_type,
                allow_no_value=allow_no_value,
                delimiters=delimiters,
                comment_prefixes=comment_prefixes,
                inline_comment_prefixes=inline_comment_prefixes,
                strict=strict,
                empty_lines_in_values=empty_lines_in_values,
                default_section=default_section,
                interpolation=interpolation
            )
        else:
            super(CompConfigParser, self).__init__(
                defaults=defaults,
                dict_type=dict_type,
                allow_no_value=allow_no_value
            )

    def read_string(self, string, source='<string>'):
        """
        Parse configuration data from a string.

        :param string: string to be parsed
        :param source: context-specific name of the string passed
        """
        if sys.version_info >= (3, 2, 0):
            super(CompConfigParser, self).read_string(string, source)
        else:
            sfile = io.StringIO(to_str(string))
            self.readfp(sfile, filename=source)
