# -*- coding: utf-8 -*-
"""
    test.t_utils.test_file
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import tempfile
from unittest import TestCase
from magrathea.utils.file import open_file


class TestMagratheaUtilsFile(TestCase):
    """
    Unit tests for :py:mod:`magrathea.utils.file`
    """

    def test_01(self):
        """
        Test Case 01:
        Try opening an existing file using the :py:func:`magrathea.utils.file.open_file` function.

        Test is passed if content can be read from file object and meets expectation.
        """
        fp, name = tempfile.mkstemp()
        os.write(fp, b"test string")
        os.close(fp)
        fd = open_file(name, 'r')
        result = fd.read()
        fd.close()
        os.unlink(name)
        self.assertEqual(result, "test string")
