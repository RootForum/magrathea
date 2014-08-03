# -*- coding: utf-8 -*-
"""
    magrathea.cli
    ~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from .dispatch import CommandDispatcher


def execute(argv=None):
    """
    Function being called from the executable to launch the CLI.
    This is the initial entrance point for any Magrathea processing.
    Usually, this function is invoked by an executable Python script
    to start the actual Magrathea CLI process. This could look like the
    following example::

       import sys
       from magrathea.cli import execute

       sys.exit(execute(sys.argv))

    :param list argv: list of (command line) arguments
    """
    dispatcher = CommandDispatcher(argv)
    dispatcher.execute()
    return dispatcher.status
