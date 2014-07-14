# -*- coding: utf-8 -*-
"""
    magrathea.utils.singleton
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""


class Singleton:
    """
    Decorator class to turn any other class into a lazy singleton.
    This class must be applied as a decorator instead of inheriting from this class.

    **Restrictions**

    * The decorated class can define one ``__init__`` function, but this constructor
      is restricted to the ``self``, ``*args`` and ``**kwargs`` arguments (in fact those must be present).
    * To get the singleton instance, the :py:meth:`~magrathea.utils.singleton.Singleton.get_instance`
      method has to be used. Trying to use ``__call__`` will result in a :py:exc:`TypeError` being raised.
    * The actual instance will not be created before :py:meth:`~magrathea.utils.singleton.Singleton.get_instance`
      has been called (lazy behaviour).
    * The decorated class cannot be inherited from. Therefore, this decorator can only be applied to final classes.
    * This decorator shows good manners and takes care of ``__doc__``, ``__module__``, ``__name__``, ``__annotations__``
      and ``__qualname__`` context of the decorated class. This allows care-free handling in conjunction with
      automated documentation extraction tools such as Sphinx autodoc or similar.

    :param decorated: The Python class to be wrapped.
    """

    _instance = None

    def __init__(self, decorated):
        self._decorated = decorated
        if hasattr(decorated, '__doc__'):
            self.__doc__ = decorated.__doc__
        if hasattr(decorated, '__module__'):
            self.__module__ = decorated.__module__
        if hasattr(decorated, '__name__'):
            self.__name__ = decorated.__name__
        if hasattr(decorated, '__annotations__'):
            self.__annotations__ = decorated.__annotations__
        if hasattr(decorated, '__qualname__'):
            self.__qualname__ = decorated.__qualname__
        if hasattr(decorated, '__mro__'):
            self.__mro__ = decorated.__mro__

    def get_instance(self, *args, **kwargs):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its ``__init__`` method.
        On all subsequent calls, the already created instance is returned.

        :param args:      positional arguments to be passed to the wrapped class' constructor
        :param kwargs:    keyword arguments to be passed to the wrapped class' constructor
        :return:          instance of the singleton-decorated class.
        """
        if not self._instance:
            self._instance = self._decorated(*args, **kwargs)
        return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `get_instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)