# -*- coding: utf-8 -*-
"""
    magrathea.cli.base
    ~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os


class BaseCommand(object):
    """
    The base class from which all CLI commands derive.

    Attributes affecting the behaviour of a Command object:

    ``help``
        A short description of the command, which will be used
        to construct help messages or usage instructions for the
        command.

    ``name``
        The name under which the command is known. Internally, the name only
        differs from an alias in the fact that it's used as the "main" alias
        in help and usage messages.

    ``aliases``
        A tuple of alias names for the command

    ``arguments``
        A tuple of arguments accepted by the command. Each argument
        consists of a tuple with two elements.
        The first element is a tuple containing the short and long
        option identifiers; e. g. ('-f', '--foo')
        The second element is a dictionary containing arbitrary elements.
        All keyword arguments accepted by :py:meth:`argparse.ArgumentParser.add_argument`
        are allowed as key names within this dictionary.
    """

    help = ''
    name = ''
    aliases = ()
    arguments = ()

    def __init__(self, global_args=None, cmd_args=None, logger=None):
        self._status = os.EX_OK
        self._global_args = global_args
        self._cmd_args = cmd_args
        self._logger = logger
        if self.get_global_argument('dir'):
            self._working_directory = self.get_global_argument('dir')
        else:
            self._working_directory = os.path.normpath(os.getcwd())

    def get_global_argument(self, name):
        """Get a global argument value"""
        if self._global_args and name in self._global_args and hasattr(self._global_args, name):
            return getattr(self._global_args, name)
        else:
            return None

    def get_command_argument(self, name):
        """Get a command argument value"""
        if self._cmd_args and name in self._cmd_args and hasattr(self._cmd_args, name):
            return getattr(self._cmd_args, name)
        else:
            return None

    def log(self, level, message):
        """Logging shortcut for convenience"""
        self._logger.log(level, message)

    def log_error(self, message):
        """Error logging short cut method for convenience"""
        self._logger.log_error(message)

    def log_warning(self, message):
        """Warning logging short cut method for convenience"""
        self._logger.log_warning(message)

    def log_notice(self, message):
        """Notice logging short cut method for convenience"""
        self._logger.log_notice(message)

    def log_info(self, message):
        """Info logging short cut method for convenience"""
        self._logger.log_info(message)

    def log_debug(self, message):
        """Debug logging short cut method for convenience"""
        self._logger.log_debug(message)

    def execute(self):
        """
        Set up environment for running the command. Then call the
        handle() method which needs to be implemented by each command.
        """
        self.handle()

    def handle(self):
        """
        The handle method contains the actual code for the command.
        This method needs to be implemented for each command.
        """
        self._status = os.EX_UNAVAILABLE
        raise NotImplementedError

    @property
    def working_directory(self):
        return self._working_directory

    @property
    def args(self):
        return self._cmd_args

    @property
    def status(self):
        return self._status
