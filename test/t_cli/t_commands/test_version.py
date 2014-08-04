# -*- coding: utf-8 -*-
"""
    test.t_cli.t_commands.test_version
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from unittest import TestCase
from magrathea.cli.base import BaseCommand
from magrathea.cli.commands.version import VersionCommand


class TestMagratheaCliCommandsVersion(TestCase):
    """
    Unit tests for :py:mod:`magrathea.cli.commands.version`
    """

    def test_01(self):
        """
        Test Case 01:
        Check if :py:class:`~magrathea.cli.commands.version.VersionCommand` is a subclass of
        :py:class:`~magrathea.cli.commands.base.BaseCommand`.

        Test is passed if :py:class:`~magrathea.cli.commands.version.VersionCommand` is a subclass of
        :py:class:`~magrathea.cli.commands.base.BaseCommand`.
        """
        self.assertTrue(issubclass(VersionCommand, BaseCommand))

    def test_02(self):
        """
        Test Case 02:
        Try creating an instance of :py:class:`~magrathea.cli.commands.version.VersionCommand`.

        Test is passed if instance proves being an instance of
        :py:class:`~magrathea.cli.commands.version.VersionCommand`.
        """
        obj = VersionCommand()
        self.assertIsInstance(obj, VersionCommand)
