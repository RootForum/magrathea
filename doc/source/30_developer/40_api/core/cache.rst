Cache Module
============

Magrathea uses a persistent cache for storing already downloaded feed items, and intermediate or
final result items occurring during the build process (at least as long as they are reusable and
accelerate the build process once available). This persistent cache is implemented as subclass
of :py:class:`~magrathea.utils.dynamic.DynamicIterable`, enhanced by corresponding hooks keeping
the iterable Python object in sync with its persistent storage backend.

.. module:: magrathea.core.cache
   :synopsis: Magrathea's cache module

.. py:currentmodule:: magrathea.core.cache

.. autoclass:: magrathea.core.cache.Cache
   :members:

Maintenance Methods
-------------------

.. method:: magrathea.core.cache.Cache.erase

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


.. method:: magrathea.core.cache.Cache.reset

   Perform a soft erase of the contents of the cache. This is done by
   deleting all items from the cache object, using its standard delete
   proceedings (including hooks for syncing deletion to the backend).

   Other than :py:meth:`~magrathea.core.cache.Cache.erase`, this method
   does not touch the database file, but sticks completely to using the
   external :py:func:`del` interface. However, this also means this
   method will fail in cases the database file is damaged or otherwise
   not properly accessible (e. g. due to format changes).


.. method:: magrathea.core.cache.Cache.sanitize

   Try repairing the backing database file by deleting it and re-syncing
   available cache content into the file. Only data already present within
   the cache object's ``self.data`` dictionary can be re-synced into the
   database. This usually is the case for all data that has been inserted,
   updated or queried through this cache object instance.

   .. warning::

      This will most probably lead to a loss of cached data, since the
      cache object usually behaves lazily. Therefore, data only present
      within the database and not yet loaded will be lost.
