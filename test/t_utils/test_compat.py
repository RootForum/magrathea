# -*- coding: utf-8 -*-
"""
    test.t_utils.test_compat
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from __future__ import unicode_literals

import os
import shutil
import tempfile
import stat
from unittest import TestCase
from magrathea.conf import get_conf
from magrathea.utils.compat import comp_makedirs, comp_open, CompConfigParser
from magrathea.utils.convert import to_bytes


class TestMagratheaUtilsCompat(TestCase):
    """
    Unit tests for :py:mod:`magrathea.utils.compat`
    """

    def test_01(self):
        """
        Test Case 01:
        Create a yet non-existing directory

        Test is passed if directory is created.
        """
        td = tempfile.mkdtemp()
        target = os.path.join(td, 'testpath')
        comp_makedirs(target)
        self.assertTrue(os.path.exists(target) and os.path.isdir(target))
        shutil.rmtree(td)

    def test_02(self):
        """
        Test Case 02:
        Create an already existing directory with the same mode and ``exist_ok`` set to True

        Test is passed if no exception is raised.
        """
        td = tempfile.mkdtemp()
        mode = stat.S_IMODE(os.stat(td).st_mode)
        flag = True
        try:
            comp_makedirs(td, mode=mode, exist_ok=True)
        except OSError:
            flag = False
        shutil.rmtree(td)
        self.assertTrue(flag)

    def test_03(self):
        """
        Test Case 03:
        Create an already existing directory with a different mode and ``exist_ok`` set to True

        Test is passed if no exception is raised.
        """
        td = tempfile.mkdtemp()
        mode = stat.S_IMODE(os.stat(td).st_mode)
        if mode == 0o700:
            mode = 0o755
        else:
            mode = 0o700
        flag = True
        try:
            comp_makedirs(td, mode=mode, exist_ok=True)
        except OSError:
            flag = False
        shutil.rmtree(td)
        self.assertTrue(flag)

    def test_04(self):
        """
        Test Case 04:
        Create an already existing directory with ``exist_ok`` set to False

        Test is passed if :py:exc:`OSError` is raised
        """
        td = tempfile.mkdtemp()
        with self.assertRaises(OSError):
            comp_makedirs(td, exist_ok=False)
        shutil.rmtree(td)

    def test_05(self):
        """
        Test Case 05:
        Open a file using :py:func:`magrathea.utils.compat.comp_open`.

        Test is passed if file content can be read and equals the given input.
        """
        test_string = "String with Ünicøde characters"
        fp, name = tempfile.mkstemp()
        os.write(fp, to_bytes(test_string))
        os.close(fp)
        fd = comp_open(name, mode='r', encoding=get_conf('DEFAULT_CHARSET'))
        result_string = fd.read()
        fd.close()
        os.unlink(name)
        self.assertEqual(test_string, result_string)

    def test_06(self):
        """
        Test Case 06:
        Use :py:func:`magrathea.utils.compat.comp_open` as :py:keyword:`with` statement context manager.

        Test is passed if file content can be read, equals the given input and the file pointer is closed.
        """
        test_string = "String with Ünicøde characters"
        fp, name = tempfile.mkstemp()
        os.write(fp, to_bytes(test_string))
        os.close(fp)
        with comp_open(name, mode='r', encoding=get_conf('DEFAULT_CHARSET')) as fd:
            result_string = fd.read()
        os.unlink(name)
        self.assertTrue(fd.closed)
        self.assertEqual(test_string, result_string)

    def test_07(self):
        """
        Test Case 07:
        Try instantiating :py:class:`magrathea.utils.compat.CompConfigParser`.

        Test is passed if instance proves being an instance of :py:class:`magrathea.utils.compat.CompConfigParser`.
        """
        obj = CompConfigParser()
        self.assertIsInstance(obj, CompConfigParser)

    def test_08(self):
        """
        Test Case 08:
        Read simple configuration from file.

        Test is passed if expected information is present within
        :py:class:`magrathea.utils.compat.CompConfigParser` object.
        """
        test_string = "[test]\nfoo = bar"
        fp, name = tempfile.mkstemp()
        os.write(fp, to_bytes(test_string))
        os.close(fp)
        obj = CompConfigParser()
        obj.read(name)
        os.unlink(name)
        self.assertTrue(obj.has_section('test'))
        self.assertTrue(obj.has_option('test', 'foo'))
        self.assertEqual(obj.get('test', 'foo'), 'bar')

    def test_09(self):
        """
        Test Case 09:
        Read simple configuration from string.

        Test is passed if expected information is present within
        :py:class:`magrathea.utils.compat.CompConfigParser` object.
        """
        test_string = "[test]\nfoo = bar"
        obj = CompConfigParser()
        obj.read_string(test_string)
        self.assertTrue(obj.has_section('test'))
        self.assertTrue(obj.has_option('test', 'foo'))
        self.assertEqual(obj.get('test', 'foo'), 'bar')
