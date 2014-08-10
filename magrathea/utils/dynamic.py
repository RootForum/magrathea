# -*- coding: utf-8 -*-
"""
    magrathea.utils.dynamic
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import sys
if sys.version_info >= (3, 0, 0):
    from collections import UserDict
else:
    from UserDict import UserDict


class Dynamic(object):
    """
    Dynamic class generating properties from kwargs
    """

    def __init__(self, *args, **kwargs):
        """
        Construct properties from keyword arguments
        """
        for elem in kwargs:
            self.__add_property(elem, kwargs[elem])

    def __add_property(self, name, value, doc=None):
        """
        Dynamically add property (read-only) to the current class object
        """
        fget = lambda self: self._get_property(name)
        setattr(self.__class__, name, property(fget, doc=doc))
        setattr(self, '_' + name, value)

    def _get_property(self, name):
        """
        Get property by its internal name
        """
        return getattr(self, '_' + name)


class DynamicIterable(UserDict, object):
    """
    A dynamic iterable object is similar to a normal Python dictionary, except it offers
    all keys also as properties.

    .. note::

       Since :py:class:`~UserDict.UserDict` in Python 2.x is an old-style class, this class
       also inherits from `object` to become a new style class.

    :param dict dict: dictionary with initial data to be filled in
    :param kwargs:    keyword arguments to be transformed into dictionary data
    """

    def __init__(self, dict=None, **kwargs):
        self._hooks = {
            'pre-set': [],
            'post-set': [],
            'pre-get': [],
            'post-get': [],
            'pre-del': [],
            'post-del': []
        }
        super(DynamicIterable, self).__init__(dict=dict, **kwargs)

    def register_hook(self, hook_type, method):
        """
        Register a hook within the corresponding hook queue.

        :param str hook_type: one of `pre-set`, `post-set`, `pre-del`, `post-del`,
                              `pre-get`, `post-get`
        :param method: reference to a method or function taking two arguments (key, value)
                       and returning exactly this tuple (however, with different content if
                       necessary to fulfil the hook's purpose).
        """
        if hook_type in self._hooks.keys():
            self._hooks[hook_type].append(method)

    def __run_hooks(self, hook_type, key, value):
        """
        Run all hooks registered to the chain of a specific hook type.

        :param str hook_type: one of `pre-set`, `post-set`, `pre-del`, `post-del`, `pre-get`, `post-get`
        :param key: initial value for `key`
        :param value: initial value for `value`
        :returns: tuple of key and value, updated by hooks.
        :rtype: tuple
        """
        chain = None
        if hook_type in self._hooks.keys():
            chain = self._hooks[hook_type]
        if chain:
            for hook in chain:
                key, value = hook(key, value)
        return key, value

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
        Overrides default ``__setitem__`` method. Functionality is identical, except a property with
        the key name is created or updated, and corresponding pre-set and post-set hooks are run.
        """
        key, item = self.__run_hooks('pre-set', key, item)
        self.__add_property(key, item)
        super(DynamicIterable, self).__setitem__(key, item)
        self.__run_hooks('post-set', key, item)

    def __delitem__(self, key, **kwargs):
        """
        Overrides default ``__delitem__`` method. Functionality is identical, the property with
        the key name is deleted and corresponding pre-del and post-del hooks are run.
        """
        key, item = self.__run_hooks('pre-del', key, self[key])
        if key in self:
            self.__del_property(key)
            super(DynamicIterable, self).__delitem__(key)
        self.__run_hooks('post-del', key, item)

    def __getitem__(self, key):
        """
        Overrides default ``__getitem__`` method. Functionality is identical, except the pre-get and
        post-get hooks are being executed.
        """
        key, item = self.__run_hooks('pre-get', key, None)
        item = super(DynamicIterable, self).__getitem__(key)
        key, item = self.__run_hooks('post-get', key, item)
        return item

    def __contains__(self, key):
        """
        Overrides default ``__contains__`` method. Function is identical, except the pre-get
        hooks are being executed.
        """
        key, item = self.__run_hooks('pre-get', key, None)
        return super(DynamicIterable, self).__contains__(key)

    def __getattr__(self, key):
        """
        Overrides default ``__getattr__`` method. Function is identical, except the pre-get
        hooks are being executed.
        """
        if key in self:
            return self[key]
        else:
            raise AttributeError
