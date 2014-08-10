# -*- coding: utf-8 -*-
"""
    magrathea.core.cache
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import shelve
from ..conf import get_conf
#from ..utils.singleton import Singleton
from ..utils.dynamic import DynamicIterable


#@Singleton
class Cache(DynamicIterable):
    """
    Class providing Magrathea's planetary cache.

    :param str db_file: Path to the database file to be used for backing this cache object
    """

    #: name of the database file to be used
    _db_file = None

    #: protocol version to use for :py:mod:`pickle`
    _protocol = 0

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._db_file = args[0]
        else:
            self._db_file = get_conf('PLANET_CACHE_FILE')
        self._protocol = get_conf('PICKLE_PROTOCOL')
        # noinspection PyTypeChecker
        super(Cache, self).__init__(dict=None, **kwargs)
        self.register_hook('pre-get', self.__hook_get_sync)
        self.register_hook('post-set', self.__hook_set_sync)
        self.register_hook('post-del', self.__hook_del_sync)

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
        """
        with shelve.open(self._db_file, flag='c', protocol=self._protocol, writeback=True) as db:
            temp_dict = dict(db)
        self.update(temp_dict)
        return super(DynamicIterable, self).__repr__()

    def __hook_get_sync(self, key, value):
        """
        Hook ensuring data not yet existing within the cache object are loaded from the database
        when looked up.

        To be applied as pre-get hook.
        """
        if key not in self.data:
            with shelve.open(self._db_file, flag='c', protocol=self._protocol, writeback=True) as db:
                try:
                    super(DynamicIterable, self).__setitem__(key, db[key])
                except KeyError:
                    pass
        return key, value

    def __hook_set_sync(self, key, value):
        """
        Hook ensuring inserted data is synced into the backing shelve database.

        To be applied as post-set hook.
        """
        with shelve.open(self._db_file, flag='c', protocol=self._protocol, writeback=True) as db:
            db[key] = value
        return key, value

    def __hook_del_sync(self, key, value):
        """
        Hook ensuring data deletion is synced to the backing shelve database.

        To be applied as post-del hook.
        """
        with shelve.open(self._db_file, flag='c', protocol=self._protocol, writeback=True) as db:
            del db[key]
        return key, value
