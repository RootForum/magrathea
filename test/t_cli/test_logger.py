# -*- coding: utf-8 -*-
"""
    test.t_cli.test_logger
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import sys
import tempfile
from unittest import TestCase, skipIf
from magrathea.cli.logger import Logger


class TestMagratheaCliLogger(TestCase):
    """
    Unit tests for :py:mod:`magrathea.cli.logger`
    """

    @skipIf(sys.version_info < (3, 0, 0), "Singleton instance recognition only works in Python 3")
    def test_01(self):
        """
        Test Case 01:
        Try getting an instance of :py:class:`~magrathea.cli.logger.Logger`.

        Test is passed if instance is an instance of :py:class:`~magrathea.cli.logger.Logger`.
        """
        obj = Logger.get_instance()
        self.assertIsInstance(obj, Logger)

    def test_02(self):
        """
        Test Case 02:
        Test logger by logging a test message into a file.

        Test is passed if file content meets expectation.
        """
        fd, name = tempfile.mkstemp()
        os.close(fd)
        logger = Logger.get_instance()
        logger.file = name
        logger.type = 'file'
        logger.log_error("This is a test message")
        logger.type = 'term'
        fp = open(name, 'r')
        content = fp.read()
        fp.close()
        os.unlink(name)
        self.assertRegexpMatches(
            content,
            r'^\[\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}\] \[ERROR\] This is a test message$'
        )
