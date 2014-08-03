# -*- coding: utf-8 -*-
"""
    magrathea.cli.dispatch
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import argparse
import sys
import os
from ..utils import loader
from .logger import Logger, Levels
from .base import BaseCommand


class CommandDispatcher(object):
    """
    Class encapsulating the logic for starting a command.

    :param list argv: list of (command line) arguments
    """

    _arguments = (
        (
            ('-d', '--dir'),
            {
                'help': 'Magrathea working directory (defaults to current work directory)',
                'action': 'store',
                'metavar': '<path>'
            }
        ),
        (
            ('-f', '--file'),
            {
                'help': 'log into file instead of the terminal',
                'action': 'store',
                'metavar': '<file>'
            }
        ),
        (
            ('-h', '--help'),
            {
                'help': 'show this help message and exit',
                'action': 'store_true',
            }
        ),
        (
            ('-l', '--loglevel'),
            {
                'help': 'the log level defines the application\'s verbosity',
                'action': 'store',
                'metavar': '<loglevel>',
                'choices': Levels
            }
        ),
        (
            ('-n', '--no-color'),
            {
                'help': 'do not colorize output',
                'action': 'store_true'
            }
        ),
        (
            ('-s', '--syslog'),
            {
                'help': 'log via syslog instead of the terminal',
                'action': 'store_true'
            }
        )
    )

    def __init__(self, argv=None):
        self._logger = Logger.get_instance()
        self._argv = argv or sys.argv[:]
        self._prog = os.path.basename(self._argv[0])
        self._status = os.EX_OK
        self._commands = {}
        self._aliases = {}
        self._get_commands()
        self._global_args = []
        self._command = ''
        self._command_args = []
        self._set_command()

    def _get_commands(self):
        """
        Detect available command modules or packages and their alias names
        """
        cmds = loader.detect_class_modules('magrathea.cli.commands', BaseCommand)
        for cmd in cmds:
            cmd_class = loader.load_member(cmds[cmd], cmd)
            self._commands[cmd_class.name] = cmd_class
            for alias in cmd_class.aliases:
                if alias in self._aliases or alias in self._commands:
                    raise AttributeError("command alias {} already exists".format(alias))
                self._aliases[alias] = cmd_class.name

    def _set_command(self):
        """
        Split arguments into global and command specific ones
        and detect the command or alias
        """
        if len(self._argv) > 1:
            for arg in self._argv[1:]:
                if arg in self._commands or arg in self._aliases:
                    position = self._argv.index(arg)
                    self._global_args = self._argv[1:position]
                    if arg in self._commands:
                        self._command = arg
                    elif arg in self._aliases:
                        self._command = self._aliases[arg]
                    position += 1
                    if len(self._argv) > position:
                        self._command_args = self._argv[position:]
            if not (self._global_args or self._command):
                self._global_args = self._argv[1:]

    @staticmethod
    def _assemble_args(arguments, indent):
        """
        Assemble argument list with a given indentation
        """
        result = ""
        maxlen = 80 - indent
        argline = ""
        argtext = ""
        for arg in arguments:
            if 'action' in arg[1]:
                if arg[1]['action'] in ('store_true', 'store_false', 'store_const', 'append_const', 'count'):
                    argtext = " [{short}|{long}]".format(short=arg[0][0], long=arg[0][1])
                elif arg[1]['action'] in ('store', 'append'):
                    argtext = " [{short} {var}]".format(short=arg[0][0], var=arg[1]['metavar'])
                if len(argtext) + len(argline) > maxlen:
                    if result:
                        result += ("\n" + indent * " ")
                    result += argline
                    argline = ""
                else:
                    argline += argtext
        if result:
            result += ("\n" + indent * " ")
        result += argline
        return result

    @staticmethod
    def _assemble_options(arguments):
        """
        Assemble options list from an arguments tuple
        """
        result = ""
        for arg in arguments:
            if len(arg) > 1:
                if 'help' in arg[1]:
                    help_text = arg[1]['help']
                else:
                    help_text = 'no description available'
                if arg[1]['action'] in ('store', 'append'):
                    result += "  {: <20s}   {: <55s}\n".format(
                        ', '.join(arg[0]) + " " + arg[1]['metavar'],
                        help_text
                    )
                else:
                    result += "  {: <20s}   {: <55s}\n".format(', '.join(arg[0]), help_text)
            elif len(arg) == 1:
                result += "  {: <20s}   {: <55s}\n".format(', '.join(arg[0]), 'no description available')
        return result

    def global_usage(self):
        """
        Create the appropriate global usage message
        """
        indent = len(self._prog) + 7
        usage_message = "usage: {executable}".format(executable=self._prog)
        if self._arguments:
            usage_message += "{arguments}".format(arguments=self._assemble_args(self._arguments, indent))
        if len(usage_message.splitlines()[-1]) + 19 > 80:
            usage_message += ("\n" + indent * " ")
        usage_message += " <command> [<args>]"
        usage_message += "\n\nAvailable commands:\n"
        for cmd in self._commands:
            usage_message += "  {: <20s}   {: <55s}\n".format(cmd, self._commands[cmd].help)
        if len(self._arguments) > 0:
            usage_message += "\nAvailable global options:\n"
            usage_message += self._assemble_options(self._arguments)
        usage_message += "\nUse '{prog} help <command>' to learn more about a specific command.".format(prog=self._prog)
        return usage_message

    def command_usage(self):
        """
        Create the appropriate command usage message
        """
        usage_message = "usage: {prog} {command}".format(prog=self._prog, command=self._command)
        indent = len(usage_message)
        if self._commands[self._command].arguments:
            usage_message += "{arguments}".format(
                arguments=self._assemble_args(self._commands[self._command].arguments, indent)
            )
        if self._commands[self._command].aliases:
            usage_message += "\n\nAliases: "
            for alias in self._commands[self._command].aliases:
                usage_message += (alias + ", ")
            usage_message = usage_message[:-2]
        if self._commands[self._command].arguments:
            usage_message += "\n\nAvailable command options:\n"
            usage_message += self._assemble_options(self._commands[self._command].arguments)
        return usage_message

    def help(self):
        """
        Reply to a user's help request
        """
        if not self._command:
            self._logger.log_usage(self.global_usage())
        else:
            self._logger.log_usage(self.command_usage())

    def execute(self):
        """
        Based on the given command line arguments and the available subcommands,
        this method creates the appropriate command line parser and starts the
        corresponding subcommand.
        """

        # check if the user asks for help
        if any(help_indicator in self._global_args for help_indicator in ['-h', '--help', 'help']) \
                or any(help_indicator in self._command_args for help_indicator in ['-h', '--help', 'help']):
            self.help()
            return

        # User didn't ask for help, but seems needing it
        if not self._command:
            self._status = os.EX_USAGE
            self.help()
            return

        # React on arguments
        global_parser = argparse.ArgumentParser(prog=self._prog, usage=self.global_usage()[7:], add_help=False)
        for arg in self._arguments:
            global_parser.add_argument(*arg[0], **arg[1])
        global_args = global_parser.parse_args(self._global_args)
        command_parser = argparse.ArgumentParser(prog=self._prog, usage=self.command_usage()[7:], add_help=False)
        for arg in self._commands[self._command].arguments:
            command_parser.add_argument(*arg[0], **arg[1])
        command_args = command_parser.parse_args(self._command_args)

        if 'file' in global_args and global_args.file:
            self._logger.file = global_args.file
            self._logger.type = 'file'

        if 'loglevel' in global_args and global_args.loglevel:
            self._logger.level = global_args.loglevel

        if 'no_color' in global_args and global_args.no_color:
            self._logger.color = False

        if 'syslog' in global_args and global_args.syslog:
            self._logger.type = 'syslog'

        # Create an instance of the called command and execute it
        command_class = self._commands[self._command]
        command = command_class(global_args=global_args, cmd_args=command_args, logger=self._logger)
        command.execute()
        self._status = command.status

    @property
    def status(self):
        """
        Exit status
        """
        return self._status
