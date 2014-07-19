# -*- coding: utf-8 -*-
"""
    magrathea.utils.termcolor
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import sys


def supports_color():
    """
    Test if the running system's terminal supports color output.

    :return: True if colors are supported, otherwise False
    :rtype:  bool
    """
    return_value = sys.platform != 'Pocket PC'
    return_value = return_value and (sys.platform != 'win32' or 'ANSICON' in os.environ)
    return_value = return_value and hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return return_value
