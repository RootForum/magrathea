# -*- coding: utf-8 -*-
"""
    test.t_cli.t_commands.test_version
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from unittest import TestCase
from magrathea.cli.base import BaseCommand
from magrathea.cli.commands.init import InitCommand


class TestMagratheaCliCommandsInit(TestCase):
    """
    Unit tests for :py:mod:`magrathea.cli.commands.init`
    """

    def test_01(self):
        """
        Test Case 01:
        Check if :py:class:`~magrathea.cli.commands.init.InitCommand` is a subclass of
        :py:class:`~magrathea.cli.commands.base.BaseCommand`.

        Test is passed if :py:class:`~magrathea.cli.commands.init.InitCommand` is a subclass of
        :py:class:`~magrathea.cli.commands.base.BaseCommand`.
        """
        self.assertTrue(issubclass(InitCommand, BaseCommand))

    def test_02(self):
        """
        Test Case 02:
        Try creating an instance of :py:class:`~magrathea.cli.commands.init.InitCommand`.

        Test is passed if instance proves being an instance of
        :py:class:`~magrathea.cli.commands.init.InitCommand`.
        """
        obj = InitCommand()
        self.assertIsInstance(obj, InitCommand)
