# -*- coding: utf-8 -*-
"""
    magrathea
    ~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""


VERSION = (0, 1, 0, 'alpha', 0)
COPYRIGHT = ('2014', 'the RootForum.org team')


def get_version(*args, **kwargs):
    """
    Returns PEP 386 compliant version number for the ControlBeast package
    """
    from .utils.version import get_version
    return get_version(*args, **kwargs)


def get_development_status(*args, **kwargs):
    """
    Returns PEP 301 compliant development status trove identifier for the ControlBeast package
    """
    from .utils.version import get_development_status
    return get_development_status(*args, **kwargs)
