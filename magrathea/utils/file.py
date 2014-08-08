# -*- coding: utf-8 -*-
"""
    magrathea.utils.file
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import sys
import warnings
from ..conf import get_conf


def open_file(file, mode='r', encoding=None):
    """
    Open a file and return a corresponding file object

    .. warning::

       This function is considered deprecated and will be removed
       in future versions of Magrathea.
       Use :py:func:`magrathea.utils.compat.comp_open` instead!

    :param str file: pathname of the file to be opened
    :param str mode: specifies the mode in which the file is opened
    :return: file object
    """
    warnings.warn(
        "The `file.open_file` function has been replaced by"
        "`compat.comp_open` and will be removed in future versions."
        "Consider using `compat.comp_open` instead of `file.open_file`.",
        category=DeprecationWarning
    )
    if sys.version_info < (3, 0, 0):
        return open(file, mode=mode)
    else:
        encoding = encoding or get_conf('DEFAULT_CHARSET')
        return open(file, mode=mode, encoding=encoding)


class File(object):
    """
    Meta class providing methods for classes that have to deal with file system objects.
    """

    @staticmethod
    def _check_access(path, mode):
        """
        Checks if a file system object can be accessed in a specific mode.

        On platforms supporting effective user and group IDs, the tests are performed
        against the effective IDs in order to respecting an eventually set SUID bit.

        :param str path: name of the file system object to be tested
        :param int mode: access mode to be tested. Should be :py:data:`os.F_OK` to test the
                         existence of *path*, or it can be the inclusive OR of one or
                         more of :py:data:`os.R_OK`, :py:data:`os.W_OK`, and :py:data:`os.X_OK`
                         to test permissions
        :returns: True if file system object can be accessed in the indicated mode, False if not.
        :rtype: bool
        """
        if hasattr(os, 'supports_effective_ids') and os.access in os.supports_effective_ids:
            # noinspection PyArgumentList
            status = os.access(path, mode, effective_ids=True)
        else:
            status = os.access(path, mode)
        return status

    @staticmethod
    def _check_file_exists(file):
        """
        Checks if a file system object exists and is a regular file.

        :param str file: name of the file system object to be tested
        :returns: True if file system object exists and is a regular file, False if not.
        :rtype: bool
        """
        return os.path.exists(os.path.abspath(file)) and os.path.isfile(os.path.abspath(file))

    @staticmethod
    def _check_dir_exists(path):
        """
        Checks if a file system object exists and is a directory.

        :param str path: name of the file system object to be tested
        :returns: True if file system object exists and is a directory, False if not.
        :rtype: bool
        """
        return os.path.exists(os.path.abspath(path)) and os.path.isdir(os.path.abspath(path))
