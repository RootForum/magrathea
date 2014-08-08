# -*- coding: utf-8 -*-
"""
    magrathea.utils.timer
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import time
import sys


def counter():
    """
    Return the value (in fractional seconds) of a performance counter with the best resolution available.

    The counter actually used depends on the platform and Python version:

    * For Python versions >=3.3, :py:func:`time.perf_counter` is used.
    * For Python versions < 3.3 on Windows, :py:func:`time.clock` is used.
    * For Python versions < 3.3 on other platforms, :py:func:`time.time` is used.

    :return: progressing counter value (in fractional seconds)
    :rtype:  float
    """
    if sys.version_info >= (3, 3, 0):
        return time.perf_counter()
    else:
        # TODO: Check implementation for Mac, since unit test randomly fails
        if sys.platform.startswith('win32'):
            return time.clock()
        else:
            return time.time()
