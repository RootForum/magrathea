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

         Although the :py:meth:`~magrathea.conf.ApplicationConf.get_instance` method accepts arbitrary
         positional and keyword arguments, they will be ignored by the constructor.


Default Configuration Values
----------------------------

.. module:: magrathea.conf.default
   :synopsis: Magrathea's default configuration values

.. py:currentmodule:: magrathea.conf.default


Core Settings
~~~~~~~~~~~~~

.. autodata:: magrathea.conf.default.DEFAULT_CHARSET

.. autodata:: magrathea.conf.default.DEFAULT_TEMPLATE_PATH

.. autodata:: magrathea.conf.default.DEFAULT_PICKLE_PROTOCOL


Logging Settings
~~~~~~~~~~~~~~~~

.. autodata:: magrathea.conf.default.DEFAULT_LOG_TYPE

.. autodata:: magrathea.conf.default.DEFAULT_LOG_LEVEL

.. autodata:: magrathea.conf.default.DEFAULT_LOG_FILE

.. autodata:: magrathea.conf.default.DEFAULT_LOG_FACILITY

.. autodata:: magrathea.conf.default.DEFAULT_LOG_TIMESTAMP

.. autodata:: magrathea.conf.default.DEFAULT_LOG_COLOR


Planet Structure
~~~~~~~~~~~~~~~~

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_THEME_DIR

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_BUILD_DIR

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_FILE

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CACHE_FILE


Planet Configuration
~~~~~~~~~~~~~~~~~~~~

Configuration Keys
^^^^^^^^^^^^^^^^^^

Global Keys
```````````

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_THEME_KEY

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_KEY

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_LIMIT_KEY

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_PAGINATE_KEY

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_THEME_DIR_KEY

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_BUILD_DIR_KEY

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_CACHE_FILE_KEY

Per Feed Keys
`````````````

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_FEED_AUTHOR_KEY

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_FEED_TITLE_KEY

Configuration Defaults
^^^^^^^^^^^^^^^^^^^^^^

Global Defaults
```````````````

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_THEME_VAL

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_VAL

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_LIMIT_VAL

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_PAGINATE_VAL

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_THEME_DIR_VAL

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_BUILD_DIR_VAL

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_CACHE_FILE_VAL

Per Feed Defaults
`````````````````

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_FEED_AUTHOR_VAL

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_FEED_TITLE_VAL

Policy Values
^^^^^^^^^^^^^

Allowed values for :py:data:`~magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_VAL`:

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_VAL_GLOBAL

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_VAL_LOCAL

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_VAL_HOURS

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_VAL_DAYS

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_VAL_WEEKS

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_VAL_MONTHS

.. autodata:: magrathea.conf.default.DEFAULT_PLANET_CONF_POLICY_VAL_NONE
