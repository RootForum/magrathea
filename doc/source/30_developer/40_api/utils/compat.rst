Compatibility Utility
=====================

.. module:: magrathea.utils.compat
   :synopsis: compatibility utility

.. py:currentmodule:: magrathea.utils.compat

The :py:mod:`~magrathea.utils.compat` module provides functions and classes whose interfaces have
changed with newer Python versions. This allows using the most recent interface of these functions
and classes within the Magrathea code, without hacking around all along the code. Therefore, this
module centralises all the dirty hacks which become necessary when the Python standard library
does not provide its own compatibility layer.


File and Directory Manipulation
-------------------------------

.. autofunction:: magrathea.utils.compat.comp_makedirs

.. autofunction:: magrathea.utils.compat.comp_open


Configuration Parser
--------------------

The :py:mod:`configparser` module from Python's standard library has heavily changed with Python 3.2.
Therefore, implementing a compatibility wrapper has become necessary to secure interoperability with
Python versions prior to 3.2.

.. autoclass:: CompConfigParser
   :members:
