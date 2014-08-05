Loader Utility
==============

.. module:: magrathea.utils.loader
   :synopsis: loader utility

.. py:currentmodule:: magrathea.utils.loader

The loader utility detecting and dynamically loading of class modules
during runtime. Detection can be limited to classes inheriting from
a specified class.

.. warning::

   The loader utility only works with new style classes which inherit at least
   from :py:class:`object`.

.. note::

   The loader utility works best with Python modules or packages containing
   only Python modules, and not sub-packages (recursive search does not properly
   work).


Detect Class Modules
--------------------

.. autofunction:: magrathea.utils.loader.detect_class_modules

**Example:**

.. code-block:: pycon

   >>> from magrathea.utils.loader import detect_class_modules
   >>> detect_class_modules('queue', object)
   {'deque': 'queue', 'Queue': 'queue', 'Empty': 'queue', 'PriorityQueue': 'queue', 'Full': 'queue', 'LifoQueue': 'queue'}
   >>> detect_class_modules('zlib', object)
   {'error': 'zlib'}
   >>> detect_class_modules('math', object)
   {}


Load Member
-----------

.. autofunction:: magrathea.utils.loader.load_member

**Example:**

.. code-block:: pycon

   >>> from magrathea.utils.loader import load_member
   >>> f = load_member('math', 'ceil')
   >>> f(1.4)
   2

