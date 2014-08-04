Magrathea's Application Configuration
=====================================

.. module:: magrathea.conf
   :synopsis: Magrathea's application configuration module

Magrathea's application configuration module provides an interface for accessing
built-in default configuration constants. Instead of scattering default constants
all over the application's code, default values shall be centralized in
:py:mod:`magrathea.conf.default`. This being the case, these configuration defaults
can be accessed by either the function interface, or by a class interface.

Function Interface
------------------

.. py:currentmodule:: magrathea.conf

.. autofunction:: magrathea.conf.get_conf


Class Interface
---------------

.. py:currentmodule:: magrathea.conf

.. autoclass:: magrathea.conf.ApplicationConf
   :members:

   .. method:: get_instance(*args, **kwargs)

      Obtain the reference to the instance of :py:class:`~magrathea.conf.ApplicationConf`. If no
      instance exists yet, one will be created and its reference returned.

      .. note::

         Although the :py:meth:`~magrathea.conf.ApplicationConf.get_instance` accepts arbitrary
         positional and keyword arguments, they will be ignored by the constructor.


Default Configuration Values
----------------------------

.. module:: magrathea.conf.default
   :synopsis: Magrathea's default configuration values

.. py:currentmodule:: magrathea.conf.default


Core Settings
~~~~~~~~~~~~~

.. autodata:: magrathea.conf.default.DEFAULT_CHARSET


Logging Settings
~~~~~~~~~~~~~~~~

.. autodata:: magrathea.conf.default.DEFAULT_LOG_TYPE

.. autodata:: magrathea.conf.default.DEFAULT_LOG_LEVEL

.. autodata:: magrathea.conf.default.DEFAULT_LOG_FILE

.. autodata:: magrathea.conf.default.DEFAULT_LOG_FACILITY

.. autodata:: magrathea.conf.default.DEFAULT_LOG_TIMESTAMP

.. autodata:: magrathea.conf.default.DEFAULT_LOG_COLOR
