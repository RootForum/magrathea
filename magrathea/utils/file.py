# -*- coding: utf-8 -*-
"""
    magrathea.utils.file
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import sys
from ..conf import get_conf


def open_file(file, mode='r'):
    """
    Open a file and return a corresponding file object

    :param str file: pathname of the file to be opened
    :param str mode: specifies the mode in which the file is opened
    :return: file object
    """
    if sys.version_info < (3, 0, 0):
        return open(file, mode=mode)
    else:
        return open(file, mode=mode, encoding=get_conf('DEFAULT_CHARSET'))
