Magrathea's Command Line Interface
==================================

.. module:: magrathea.cli
   :synopsis: Magrathea's command line interface

Magrathea's command line interface is contained within the
:py:mod:`magrathea.cli` package. It offers only one function at package
level which can be called directly. This function is usually called
from a Python script acting as executable interface.

.. py:currentmodule:: magrathea.cli

.. autofunction:: magrathea.cli.execute


Logging Interface
-----------------

.. module:: magrathea.cli.logger
   :synopsis: Magrathea's output interface

The :py:mod:`~magrathea.cli.logger` module is responsible for handling any
output that shall be transported to the user. It provides a class interface,
offering a flexible message output system:

.. py:currentmodule:: magrathea.cli.logger

.. autoclass:: magrathea.cli.logger.Logger
   :members:

   .. method:: get_instance(*args, **kwargs)

      Obtain the reference to the instance of :py:class:`~magrathea.cli.logger.Logger`. If no
      instance exists yet, one will be created and its reference returned.

      .. warning::

         If a logger instance already exists (e. g. due to an earlier invocation from another
         module or function), any passed keyword arguments will be ignored. Therefore, it is
         safer to not using any keyword arguments, but setting the logger's properties appropriately
         after having received the logger instance's reference.

   .. method:: log(level, message)

      Register a log message within the logging queue and flush the queue afterwards (currently
      log messages are not cached).

      :param str level:   The log level to be used for the message to be passed. Must be one of
                          *error*, *warning*, *notice*, *info*, *debug* or *usage*.
      :param str message: The message string to be recorded
