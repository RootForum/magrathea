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

