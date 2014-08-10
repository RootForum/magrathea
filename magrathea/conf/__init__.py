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

       Only uppercase configuration values are taken into account. However, when querying
       for an item, it will also be recognized if it is in lower or mixed case since this
       class takes care of converting all query keys to upper key before looking for them.

    Along with each *DEFAULT_...* configuration member, also a corresponding non-default member
    is created. E. g. alongside with *DEFAULT_CHARSET*, also the non-default *CHARSET*
    member is created. Other than *DEFAULT_* members, non-default members are mutable, so their
    values can be updated during runtime.

    .. note::

       Although non-default members are mutable, they cannot be deleted if they belong to a
       *DEFAULT_* member. Deleting them only resets them to their original DEFAULT value.

    This class is implemented following the singleton pattern. Therefore,
    in order to getting a reference to the class' instance, the
    :py:meth:`~magrathea.utils.singleton.Singleton.get_instance` method has to be used.

    Example::

       configuration = ApplicationConf.get_instance()
    """

    def __init__(self):
        # For Python 2 Compatibility, super() cannot be used
        # inside a decorated class :-(
        DynamicIterable.__init__(self)
        self.register_hook('pre-set', self._hook_uppercase)
        self.register_hook('pre-get', self._hook_uppercase)
        self.register_hook('pre-del', self._hook_uppercase)
        self.register_hook('pre-set', self._hook_defaults_not_mutable)
        self.register_hook('pre-del', self._hook_defaults_not_mutable)
        self.register_hook('pre-set', self._hook_default_create_mirror)
        self.register_hook('pre-del', self._hook_default_mirror_reset)

        # convert all upper case configuration values from :py:module:`~magrathea.conf.default`
        for setting in dir(default):
            if setting.isupper():
                self[setting] = getattr(default, setting)

    @staticmethod
    def _hook_uppercase(key, value):
        """
        Hook method ensuring that all keys are kept in upper case.

        To be applied as pre-set, pre-get and pre-del hook.
        """
        return str(key).upper(), value

    def _hook_defaults_not_mutable(self, key, value):
        """
        Hook method ensuring ``DEFAULT`` values do not get overwritten.

        To be applied as pre-set and pre-del hook.
        """
        if key.startswith('DEFAULT_') and key in self:
            raise KeyError('DEFAULT configuration settings are immutable!')
        return key, value

    def _hook_default_create_mirror(self, key, value):
        """
        Hook method ensuring for all ``DEFAULT`` values, a mutable mirror is created.

        To be applied as pre-set hook.
        """
        if key.startswith('DEFAULT_'):
            self[key[8:]] = value
        return key, value

    def _hook_default_mirror_reset(self, key, value):
        """
        Hook method ensuring that mirror values of ``DEFAULT`` entries are reset to
        their default parent instead of really being deleted.

        To be applied as pre-del hook.
        """
        if "DEFAULT_{}".format(key) in self:
            self.__setitem__(key, self["DEFAULT_{}".format(key)])
            return None, value
        else:
            return key, value
