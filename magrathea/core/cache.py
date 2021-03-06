# -*- coding: utf-8 -*-
"""
    magrathea.core.cache
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import shelve
from ..conf import get_conf
from ..utils.singleton import Singleton
from ..utils.dynamic import DynamicIterable


@Singleton
class Cache(DynamicIterable):
    """
    Class providing Magrathea's planetary cache.

    Please note that this class is decorated by the :py:class:`~magrathea.utils.singleton.Singleton`
    decorator, which means only one instance can exist. Furthermore, instances cannot
    be created directly, but must be retrieved by the ``get_instance`` method::

       cache_object = Cache.get_instance()

    The :py:class:`~magrathea.core.cache.Cache` object provides two interfaces, both
    inherited from :py:class:`magrathea.utils.dynamic.DynamicIterable`: On one hand,
    it behaves like any normal dictionary. So it can be used in the well-known way::

        >>> cache = Cache.get_instance('/tmp/my_cache')
        >>> cache['foo'] = 'bar'
        >>> 'foo' in cache
        True
        >>> cache.items()
        [('foo', 'bar')]
        >>> cache.keys()
        ['foo']
        >>> del cache['foo']
        >>> 'foo' in cache
        False

    .. note::

       The only restriction is that keys have to be strings. To avoid any conflicts,
       it is highly recommended to use only ascii character strings without any whitespace
       characters.

    On the other hand, existing items are also accessible as property, meaning they can
    be queried or modified, but not be created or deleted that way::

       >>> cache = Cache.get_instance('/tmp/my_cache')
       >>> cache['foo'] = 'bar'
       >>> hasattr(cache, 'foo')
       True
       >>> cache.foo
       'bar'
       >>> cache.foo = 'baz'
       >>> cache.foo
       'baz'
       >>> cache['foo']
       'baz'

    All insert, update and delete operations are synchronized into a :py:mod:`shelve` persistence
    storage. This storage is also consulted when asked for a specific item::

       >>> cache = Cache.get_instance('/tmp/my_cache')
       >>> 'foo' in cache
       True
       >>> hasattr(cache, 'foo')
       True
       >>> cache
       {'foo': 'baz'}

    .. warning::

       When ``hasattr`` or ``in`` are implemented lazily, meaning only the queried item is really
       loaded from the storage, accessing the cache object directly (triggering its ``__repr__``
       method) is hugely expensive, since the full content of the database is synchronized into
       the cache container object.

    :param str db_file: Path to the database file to be used for backing this cache object
    """

    #: name of the database file to be used
    _db_file = None

    #: protocol version to use for :py:mod:`pickle`
    _protocol = 0

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._db_file = args[0]
        if 'db' in kwargs:
            self._db_file = kwargs['db']
        if 'db_file' in kwargs:
            self._db_file = kwargs['db_file']
        if not self._db_file:
            self._db_file = get_conf('PLANET_CACHE_FILE')

        self._protocol = get_conf('PICKLE_PROTOCOL')

        DynamicIterable.__init__(self)
        self.register_hook('pre-get', self._hook_get_sync)
        self.register_hook('post-set', self._hook_set_sync)
        self.register_hook('post-del', self._hook_del_sync)

    def sanitize(self):
        """
        Try repairing the backing database file by deleting it and re-syncing
        available cache content into the file. Only data already present within
        the cache object's ``self.data`` dictionary can be re-synced into the
        database. This usually is the case for all data that has been inserted,
        updated or queried through this cache object instance.

        .. warning::

           This will most probably lead to a loss of cached data, since the
           cache object usually behaves lazily. Therefore, data only present
           within the database and not yet loaded will be lost.
        """
        os.unlink(self._db_file)
        db = shelve.open(self._db_file, flag='n', protocol=self._protocol, writeback=True)
        for key, value in self.data.items():
            db[key] = value
        db.close()

    def erase(self):
        """
        Perform a hard erase of the contents of the cache. This is done by
        deleting the backing database file, re-creating it and removing all
        items from ``self.data``, plus deleting the corresponding properties.

        This method also works when the backing database file itself is broken
        (e. g. has become inconsistent or the db format has changed). This is
        due to the fact that this method works around the normal internal data
        handling procedures (therefore referred to as *hard erase*).

        .. warning::

           This method should be considered as a last resort, when no other
           means for accessing the data do work. In normal operation, you
           will want to use :py:meth:`~magrathea.core.cache.Cache.reset` if
           you intend to empty a cache entirely.
        """
        self.sanitize()
        items = [item for item in self.data.keys()]
        for item in items:
            del self[item]

    def reset(self):
        """
        Perform a soft erase of the contents of the cache. This is done by
        deleting all items from the cache object, using its standard delete
        proceedings (including hooks for syncing deletion to the backend).

        Other than :py:meth:`~magrathea.core.cache.Cache.erase`, this method
        does not touch the database file, but sticks completely to using the
        external :py:func:`del` interface. However, this also means this
        method will fail in cases the database file is damaged or otherwise
        not properly accessible (e. g. due to format changes).
        """
        items = [item for item in self.keys()]
        for item in items:
            del self[item]

    def __repr__(self):
        """
        Override original ``__repr__`` method. Before returning, sync all objects from the
        database into the internal data store.

        .. warning::

           Where calls to :py:meth:`~magrathea.core.cache.Cache.__contains__` and
           :py:meth:`~magrathea.core.cache.Cache.__getattr__` behave lazily (i. e. they
           only access the backing :py:mod:`shelve` store only for retrieving one particular
           member), calling the :py:meth:`~magrathea.core.cache.Cache.__repr__` method (e. g.
           by addressing the object directly) will synchronize the full :py:mod:`shelve` store
           into the living object. This might be very time-consuming!

        .. note::

           Unfortunately, we just cannot abuse ``self.update()`` here, since in Python 2.7,
           this is implemented as ``self.data.update()``, which does not trigger the
           :py:meth:`~magrathea.utils.dynamic.DynamicIterable.__setitem__` method to be run.
           Consequently, the :py:meth:`~magrathea.utils.dynamic.DynamicIterable.__add_property`
           method is also not run, and therefore this way will end up with a correctly working
           dictionary interface, but with missing properties, having both in a non-synced state.

           Therefore, we have to resort to copying keys and values item-wise from the database
           backend. Please note that in the Python 3 implementation of :py:class:`collections.UserDict`,
           this behaviour has changed -- ``self`` is triggered directly, so the
           :py:meth:`~magrathea.utils.dynamic.DynamicIterable.__setitem__` method would be
           triggered.
        """
        db = shelve.open(self._db_file, flag='c', protocol=self._protocol, writeback=True)
        temp_dict = dict(db.items())
        db.close()
        for key, value in temp_dict.items():
            self[key] = value
        return DynamicIterable.__repr__(self)

    def _hook_get_sync(self, key, value):
        """
        Hook ensuring data not yet existing within the cache object are loaded from the database
        when looked up.

        To be applied as pre-get hook.
        """
        if key not in self.data:
            db = shelve.open(self._db_file, flag='c', protocol=self._protocol, writeback=True)
            try:
                data = db[key]
            except KeyError:
                data = None
            db.close()
            if data:
                self.__setitem__(self, key, data)
        return key, value

    def _hook_set_sync(self, key, value):
        """
        Hook ensuring inserted data is synced into the backing shelve database.

        To be applied as post-set hook.
        """
        db = shelve.open(self._db_file, flag='c', protocol=self._protocol, writeback=True)
        db[key] = value
        db.close()
        return key, value

    def _hook_del_sync(self, key, value):
        """
        Hook ensuring data deletion is synced to the backing shelve database.

        To be applied as post-del hook.
        """
        db = shelve.open(self._db_file, flag='c', protocol=self._protocol, writeback=True)
        del db[key]
        db.close()
        return key, value
