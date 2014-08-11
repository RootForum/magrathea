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

   The :py:func:`~magrathea.cli.execute` function will create a :py:class:`~magrathea.cli.dispatch.CommandDispatcher`
   instance, which provides the logic for invoking a command.


Dispatcher
----------

.. module:: magrathea.cli.dispatch
   :synopsis: Magrathea's command line dispatcher

.. py:currentmodule:: magrathea.cli.dispatch

.. autoclass:: magrathea.cli.dispatch.CommandDispatcher
   :members:


Command Line Commands
---------------------

Command line commands are implemented as modules within the :py:mod:`magrathea.cli.commands` package.
The module name itself must be unique within the :py:mod:`~magrathea.cli.commands` package, but has no
direct link to the command's external designator used on the command line.

.. module:: magrathea.cli.base
   :synopsis: base for command line commands to inherit from

All command line commands are implemented as classes, inheriting from :py:class:`magrathea.cli.base.BaseCommand`:

.. py:currentmodule:: magrathea.cli.base

.. autoclass:: magrathea.cli.base.BaseCommand
   :members:


Writing a Command Line Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Writing a command line command can be as easy as creating a Python module within the
:py:mod:`magrathea.cli.commands` package containing a class inheriting from
:py:class:`~magrathea.cli.base.BaseCommand` and overriding some basic settings:

.. code-block:: python

   from magrathea.cli.base import BaseCommand

   class MyCommand(BaseCommand)
      name = 'foo'
      aliases = ('bar', 'baz')
      help = 'The super foo command that makes you bar'

Looks easy? It actually is, since :py:class:`~magrathea.cli.dispatch.CommandDispatcher`
is performing all the black magic needed to detect available commands, make up decent usage
messages out of the information provided by each command's implementation, parsing eventual
command line arguments required by the different commands and finally setting up the environment
and running the command.

Unfortunately, this command would not be of any use -- once invoked by the dispatcher, it will
simply raise a :py:exc:`NotImplementedError` exception. This is simply for the fact that each
command needs to implement its own :py:meth:`~magrathea.cli.base.BaseCommand.handle` method.
Since this has not happened here, the :py:meth:`~magrathea.cli.base.BaseCommand.handle` method
inherited from the :py:class:`~magrathea.cli.dispatch.CommandDispatcher` class will be used, and
this one simply raises a :py:exc:`NotImplementedError` exception.

When implementing your own :py:meth:`~magrathea.cli.base.BaseCommand.handle` method, please
take care of the following conventions.

User Interaction
^^^^^^^^^^^^^^^^

Whenever possible, user interaction shall be avoided. The concept of Magrathea is to gather all
required information either form command line arguments or from configuration files, and then to
run silently, only outputting status information according to the log level set by the user.

This restriction has been set in order to respecting that one important use case is to run
Magrathea as cron job, where no user interaction is possible.

Output
^^^^^^

All output to the user interface shall be channelled through the appropriate ``log_...()`` methods
each command class has inherited from the :py:class:`~magrathea.cli.base.BaseCommand` class.
This ensures the output is only sent if the user has selected the corresponding log level, and it
is sent through the right channel.

.. warning::

   **Never** use Python's :py:func:`print` function to generate and send output to the user
   interface. This will break Magrathea's promise of being 100% cron job enabled, including
   logging its output to a file or through :py:mod:`syslog`.

Status
^^^^^^

Magrathea uses the :py:attr:`~magrathea.cli.base.BaseCommand.status` property any command
has inherited from the :py:class:`~magrathea.cli.base.BaseCommand` class for setting an
appropriate exit status when terminating Magrathea's main process.

By default, a command object's status is set to :py:data:`os.EX_OK`. If necessary or appropriate, the
status information can be changed within the :py:meth:`~magrathea.cli.base.BaseCommand.handle` method
by overwriting the internal ``_status`` member::

   def handle(self):
      self._status = os.EX_IOERR


Existing Command Line Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: magrathea.cli.commands
   :synopsis: package containing all command line commands

Init Command
^^^^^^^^^^^^

.. module:: magrathea.cli.commands.init
   :synopsis: module implementing the init command

.. py:currentmodule:: magrathea.cli.commands.init

.. autoclass:: magrathea.cli.commands.init.InitCommand
   :members:
   :undoc-members:

Version Command
^^^^^^^^^^^^^^^

.. module:: magrathea.cli.commands.version
   :synopsis: module implementing the version command

.. py:currentmodule:: magrathea.cli.commands.version

.. autoclass:: magrathea.cli.commands.version.VersionCommand
   :members:
   :undoc-members:

Logging Interface
-----------------

.. module:: magrathea.cli.logger
   :synopsis: Magrathea's output interface

The :py:mod:`~magrathea.cli.logger` module is responsible for handling any
output that shall be transported to the user. It implements the magic behind
the ``log_...()`` methods provided by the :py:class:`~magrathea.cli.dispatch.CommandDispatcher`
class, allowing command implementations to easily transporting information to the user interface.

The :py:mod:`~magrathea.cli.logger` module provides a class interface,
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

   .. method:: log_error(message)

      Convenience shortcut for registering messages with log level `error`

      :param str message: The message string to be recorded

   .. method:: log_warning(message)

      Convenience shortcut for registering messages with log level `warning`

      :param str message: The message string to be recorded

   .. method:: log_notice(message)

      Convenience shortcut for registering messages with log level `notice`

      :param str message: The message string to be recorded

   .. method:: log_info(message)

      Convenience shortcut for registering messages with log level `info`

      :param str message: The message string to be recorded

   .. method:: log_debug(message)

      Convenience shortcut for registering messages with log level `debug`

      :param str message: The message string to be recorded

   .. method:: log_usage(message)

      Convenience shortcut for registering messages with log level `usage`

      :param str message: The message string to be recorded

   .. attribute:: color

      Boolean switch indicating whether this logger allows colored output.

   .. attribute:: facility

      The facility used for syslog.

   .. attribute:: file

      The log file used when run as file logger. Must be a string indicating the
      path name of the file to log into.

   .. attribute:: level

      The log level (string). Expected to be one of `mute`, `error`, `warning`, `info` or `debug`.

   .. attribute:: type

      The logger type (string). Expected to be one of `term`, `file` or `syslog`.


