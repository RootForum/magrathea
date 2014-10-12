# -*- coding: utf-8 -*-
"""
    magrathea.cli.commands.version
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
from ..base import BaseCommand
from ...core.planet import Planet
from ...utils.file import File


class InitCommand(BaseCommand, File):
    """
    Command class implementing the version command.
    """

    name = 'init'
    aliases = ()
    help = 'Initialise an empty planet structure.'
    arguments = (
        (
            ('-P', '--no-purge'),
            {'help': 'do not remove existing content from the target directory', 'action': 'store_true'}
        ),
    )

    def handle(self):
        """Command handler for the init command"""
        planet = Planet.get_instance(self._working_directory)
        result = planet.init(purge=not self.get_command_argument('no_purge'))
        for level, message in result.messages:
            self.log(level, message)
        if not result:
            self._status = os.EX_IOERR
        else:
            self._status = os.EX_OK
