Termcolor Utility
=================

.. module:: magrathea.utils.termcolor
   :synopsis: termcolor utility

.. py:currentmodule:: magrathea.utils.termcolor

The termcolor utility provides means to detect whether a system environment technically supports
coloured output on a terminal (:py:data:`sys.stdout`) or not. It relies on information provided
by the file object itself and :py:data:`sys.platform`.

.. autofunction:: magrathea.utils.termcolor.supports_color
