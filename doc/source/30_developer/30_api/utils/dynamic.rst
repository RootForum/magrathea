Dynamic Utility
===============

.. module:: magrathea.utils.dynamic
   :synopsis: dynamic utility

The dynamic utility provides two abstract classes which are intended to be inherited from or
being used in a stand-alone mode. Both classes provide means for dynamically creating properties,
based on a given set of information.

.. py:currentmodule:: magrathea.utils.dynamic

Dynamic Class
-------------

.. autoclass:: magrathea.utils.dynamic.Dynamic
   :members:

   The constructor of the :py:class:`~magrathea.utils.dynamic.Dynamic` class uses
   all keyword arguments passed to the constructor for creating :py:func:`property`
   attributes with the same name as the keyword argument, returning the value submitted
   with the keyword argument.

**Usage Example**::

   >>> from magrathea.utils.dynamic import Dynamic
   >>> obj = Dynamic(foo='bar')
   >>> 'foo' in dir(obj)
   True
   >>> hasattr(obj, 'foo')
   True
   >>> getattr(obj, 'foo')
   'bar'
   >>> obj.foo
   'bar'

.. note::

   The properties are dynamically created by the constructor. After the constructor has
   terminated, the property set of the created object is fix (except for direct manipulation
   using :py:func:`setattr` and :py:func:`delattr`).


Dynamic Iterable Class
----------------------

The dynamic iterable class interface is much more complex than the pure :py:class:`~magrathea.utils.dynamic.Dynamic`
class. It not only provides dynamically generated :py:func:`property` attributes, but also acts as a
:py:class:`dict` instance, allowing to access all attribute values by using their names as keys. Furthermore,
attributes are dynamically created, updated or deleted when the object is manipulated via its dictionary interface.

In addition, the :py:class:`~magrathea.utils.dynamic.Dynamic` class allows for registering hook methods or
functions, which can be used to manipulate the item setting and deletion behaviour.

.. autoclass:: magrathea.utils.dynamic.DynamicIterable
   :members:

**Usage example**::

   >>> from magrathea.utils.dynamic import DynamicIterable
   >>> obj = DynamicIterable(foo='bar')
   >>> 'foo' in dir(obj)
   True
   >>> hasattr(obj, 'foo')
   True
   >>> getattr(obj, 'foo')
   'bar'
   >>> obj.foo
   'bar'
   >>> 'foo' in obj
   True
   >>> obj['foo']
   'bar'
   >>> hasattr(obj, 'fuu')
   False
   >>> obj['fuu'] = 'baz'
   >>> hasattr(obj, 'fuu')
   True


**Hooks example**::

   from magrathea.utils.dynamic import DynamicIterable
   class MyIterable(DynamicIterable):

       def __init__(self, dict=None, **kwargs):
           self.register_hook('pre-set', my_hook)
           self.register_hook('pre-get', my_hook)
           super(MyIterable, self).__init__(dict=dict, **kwargs)

       def my_hook(self, key, value)
           return key.upper(), value


This example demonstrates how one can render the DynamicIterable's keys case-agnostic.
