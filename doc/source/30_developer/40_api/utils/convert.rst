Convert Utility
===============

.. module:: magrathea.utils.convert
   :synopsis: convert utility

The convert utility functions can convert unicode strings into byte sequences and vice versa.
Independent of the Python version used, they ensure a string (as seen by the convert utilities)
is always a unicode string, and a byte sequence (as seen by the convert utilities) is always
a sequence of bytes, and not a multi-byte sequence.

.. py:currentmodule:: magrathea.utils.convert

.. autofunction:: magrathea.utils.convert.to_bytes

.. autofunction:: magrathea.utils.convert.to_str
