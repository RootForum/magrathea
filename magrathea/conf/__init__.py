# -*- coding: utf-8 -*-
"""
    magrathea.conf
    ~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""

from magrathea.conf import default
from magrathea.utils.dynamic import DynamicIterable
from magrathea.utils.singleton import Singleton


def get_conf(key):
    """
    Get a global configuration value by its key.

    :param str key: string identifying the requested configuration value
    :returns the requested configuration value or None
    """
    configuration = MagratheaConf.get_instance()
    if key.upper() in configuration:
        return configuration[key.upper()]
    else:
        return None


@Singleton
class MagratheaConf(DynamicIterable):
    """
    Global Magrathea configuration object.

    This class acts as a proxy to all configuration information set in
    :py:mod:`~magrathea.conf.default`. The configuration data can be
    accessed either as :py:func:`property` of the :py:class:`~magrathea.conf.MagratheaConf`
    object, or as *(key, value)* pair via the :py:class:`~magrathea.conf.MagratheaConf`
    dictionary interface.

    .. note::

       Only uppercase configuration values are taken into account.

    This class is implemented following the singleton pattern. Therefore,
    in order to getting a reference to the library, the
    :py:meth:`~magrathea.utils.singleton.Singleton.get_instance` method has to be used.

    Example::

       configuration = MagratheaConf.get_instance()
    """

    def __init__(self):

        # ensure the constructor of the CbDynamicIterable parent side is called
        super(DynamicIterable, self).__init__(dict=None)

        # convert all upper case configuration values from :py:module:`~magrathea.conf.default`
        for setting in dir(default):
            if setting.isupper():
                self[setting] = getattr(default, setting)