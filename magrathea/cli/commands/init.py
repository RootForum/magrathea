# -*- coding: utf-8 -*-
"""
    magrathea.cli.commands.version
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import shutil
from ..base import BaseCommand
from ...utils.compat import comp_makedirs
from ...utils.file import File
from ...core.template import Template
from ...conf import get_conf


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
        if not self.get_command_argument('no-purge'):
            self.log_debug("purging destination directory {}".format(self._working_directory))
            try:
                for item in os.listdir(self._working_directory):
                    if not self._check_dir_exists(item):
                        os.unlink(item)
                    else:
                        shutil.rmtree(item)
            except OSError as e:
                self.log_error("Error {}".format(e))
                self._status = os.EX_IOERR
                return
        if not self._check_dir_exists(self._working_directory):
            try:
                comp_makedirs(self._working_directory, exist_ok=True)
            except OSError as e:
                self.log_error("Error {}".format(e))
                self._status = os.EX_IOERR
                return
        template = Template(template=get_conf('PLANET_TEMPLATE'), path=self._working_directory)
        try:
            template.deploy()
        except RuntimeError as e:
            self.log_error("Error {}".format(e))
            self._status = os.EX_DATAERR
            return
        self._status = os.EX_OK
