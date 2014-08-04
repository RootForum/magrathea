File Utility
============

.. module:: magrathea.utils.file
   :synopsis: file utility

The file utility offers a simple wrapper for Python's :py:func:`open` function.
Wrapping the :py:func:`open` function has become necessary since Python 2 and
Python 3 provide different implementations of :py:func:`open`. Most notably, the
signature has changed. While the old arguments known already from Python 2
(``file``, ``mode`` and ``buffering``) are still valid, the Python 3 implementation
of :py:func:`open` allows supplementary (and most useful) arguments, e. g. such as
the ``encoding`` argument.

In order to not losing the advantages of the encoding argument when operating in a
Python 3 environment, this wrapper function ensures the ``encoding`` argument is
also accepted in a Python 2 environment, but will not lead to a change in behaviour
of the file descriptor returned by this wrapper function.

.. py:currentmodule:: magrathea.utils.file

.. autofunction:: magrathea.utils.file.open_file
