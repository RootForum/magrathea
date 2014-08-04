# -*- coding: utf-8 -*-
"""
    test.t_cli.test_dispatch
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import sys
from unittest import TestCase
from magrathea.cli.dispatch import CommandDispatcher


class TestMagratheaCliDispatch(TestCase):
    """
    Unit tests for :py:mod:`magrathea.cli.dispatch`
    """

    def test_01(self):
        """
        Test Case 01:
        Try getting an instance of :py:class:`~magrathea.cli.dispatch.CommandDispatcher`.

        Test is passed if instance is an instance of :py:class:`~magrathea.cli.dispatch.CommandDispatcher`.
        """
        obj = CommandDispatcher()
        self.assertIsInstance(obj, CommandDispatcher)

    def test_02(self):
        """
        Test Case 02:
        Initialise an instance of :py:class:`~magrathea.cli.dispatch.CommandDispatcher` with an existing CLI command.

        Test is passed if the command is detected correctly.
        """
        args = [sys.argv[0], 'version']
        obj = CommandDispatcher(args)
        self.assertEqual(obj._command, 'version')

    def test_03(self):
        """
        Test Case 03:
        Initialise an instance of :py:class:`~magrathea.cli.dispatch.CommandDispatcher` with an existing CLI alias.

        Test is passed if the command belonging to the alias is detected correctly.
        """
        args = [sys.argv[0], '-v']
        obj = CommandDispatcher(args)
        self.assertEqual(obj._command, 'version')

    def test_04(self):
        """
        Test Case 04:
        Initialise an instance of :py:class:`~magrathea.cli.dispatch.CommandDispatcher` with a non-existing command.

        Test is passed if the command detected remains an empty string.
        """
        args = [sys.argv[0], 'foo']
        obj = CommandDispatcher(args)
        self.assertEqual(obj._command, '')
