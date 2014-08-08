# -*- coding: utf-8 -*-
"""
    magrathea.conf
    ~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""

from . import default
from ..utils.dynamic import DynamicIterable
from ..utils.singleton import Singleton


def get_conf(key):
    """
    Get a global configuration value by its key.

    :param str key: string identifying the requested configuration value
    :returns: the requested configuration value or None
    """
    configuration = ApplicationConf.get_instance()
    if key.upper() in configuration:
        return configuration[key.upper()]
    else:
        return None


@Singleton
class ApplicationConf(DynamicIterable):
    """
    Global Magrathea configuration object.

    This class acts as a proxy to all configuration information set in
    :py:mod:`~magrathea.conf.default`. The configuration data can be
    accessed either as :py:func:`property` of the :py:class:`~magrathea.conf.ApplicationConf`
    object, or as *(key, value)* pair via the :py:class:`~magrathea.conf.ApplicationConf`
    dictionary interface.

    .. note::

       Only uppercase configuration values are taken into account.

    Along with each *DEFAULT_...* configuration member, also a corresponding non-default member
    is created. E. g. alongside with *DEFAULT_CHARSET*, also the non-default *CHARSET*
    member is created. Other than *DEFAULT_* members, non-default members are mutable, so their
    values can be updated during runtime.

    .. note::

       Although non-default members are mutable, they cannot be deleted if they belong to a
       *DEFAULT_* member. Deleting them only resets them to their original DEFAULT value.

    This class is implemented following the singleton pattern. Therefore,
    in order to getting a reference to the library, the
    :py:meth:`~magrathea.utils.singleton.Singleton.get_instance` method has to be used.

    Example::

       configuration = ApplicationConf.get_instance()
    """

    def __init__(self, *args, **kwargs):

        # ensure the constructor of the CbDynamicIterable parent side is called
        super(DynamicIterable, self).__init__(dict=None)

        # convert all upper case configuration values from :py:module:`~magrathea.conf.default`
        for setting in dir(default):
            if setting.isupper():
                self[setting] = getattr(default, setting)
                # Create a non-default setting name for default settings
                if setting.startswith('DEFAULT_'):
                    self[setting[8:]] = getattr(default, setting)

    def __add_property(self, name, value, doc=None):
        """
        Dynamically add property to the current class object
        """
        fget = lambda self: self[name]
        fset = lambda self, value: self.__setitem__(name, value)
        setattr(self.__class__, name, property(fget=fget, fset=fset, doc=doc))

    def __del_property(self, name):
        """
        Dynamically delete property and internal representation
        """
        delattr(self.__class__, name)

    def __setitem__(self, key, item, **kwargs):
        """
        Override ``__setitem__`` to make DEFAULT_ values immutable
        """
        if key in self and key.startswith('DEFAULT_'):
            raise KeyError('DEFAULT configuration settings are immutable!')
        self.__add_property(key, item)
        super(DynamicIterable, self).__setitem__(key, item)

    def __delitem__(self, key, **kwargs):
        """
        Override ``__delitem__`` to make DEFAULT_ values immutable
        """
        # Deny deletion of DEFAULT members
        if key in self and key.startswith('DEFAULT_'):
            raise KeyError('DEFAULT configuration settings are immutable!')
        # For members mirroring a DEFAULT, just reset them to their DEFAULT value
        # Only delete members which are neither DEFAULT, nor do mirror a DEFAULT.
        if "DEFAULT_{}".format(key) in self:
            self.__setitem__(key, self["DEFAULT_{}".format(key)])
        else:
            self.__del_property(key)
            super(DynamicIterable, self).__delitem__(key)
