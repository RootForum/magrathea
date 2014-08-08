# -*- coding: utf-8 -*-
"""
    test.t_utils.test_file
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import tempfile
from unittest import TestCase, skipUnless, skipIf
from magrathea.utils.file import open_file, File


class TestMagratheaUtilsFile(TestCase):
    """
    Unit tests for :py:mod:`magrathea.utils.file`
    """

    def test_01(self):
        """
        Test Case 01:
        Try opening an existing file using the :py:func:`magrathea.utils.file.open_file` function.

        Test is passed if a deprecation warning is raised, content can be read from file object
        and meets expectation.
        """
        fp, name = tempfile.mkstemp()
        os.write(fp, b"test string")
        os.close(fp)
        with self.assertWarns(DeprecationWarning):
            fd = open_file(name, 'r')
        result = fd.read()
        fd.close()
        os.unlink(name)
        self.assertEqual(result, "test string")

    def test_02(self):
        """
        Test Case 02:
        Try getting an instance of :py:class:`magrathea.utils.file.File`.

        Test is passed if instance proves being an instance of :py:class:`magrathea.utils.file.File`.
        """
        obj = File()
        self.assertIsInstance(obj, File)

    def test_03(self):
        """
        Test Case 03:
        Test :py:meth:`magrathea.utils.file.File._check_access` with an existing path (this file).

        Test is passed if return value is True.
        """
        self.assertTrue(File._check_access(__file__, os.R_OK))

    @skipIf(os.path.exists('/foobarstuffdirdoesntexist'), 'Rubbish path existing on your system. Clean up!')
    def test_04(self):
        """
        Test Case 04:
        Test :py:meth:`magrathea.utils.file.File._check_access` with a non existing path.

        Test is passed if return value is False.
        """
        self.assertFalse(File._check_access('/foobarstuffdirdoesntexist', os.R_OK))

    @skipUnless(os.path.exists('/usr/sbin'), '/usr/sbin does not exist on this system')
    def test_05(self):
        """
        Test Case 05:
        Test :py:meth:`magrathea.utils.file.File._check_access` with an existing, but forbidden path.

        Test is passed if return value is False.
        """
        self.assertFalse(File._check_access('/usr/sbin', os.W_OK))

    def test_06(self):
        """
        Test Case 06:
        Test :py:meth:`magrathea.utils.file.File._check_file_exists` with an existing file (this file).

        Test is passed if return value is True.
        """
        self.assertTrue(File._check_file_exists(__file__))

    @skipIf(os.path.exists('/foobarstuffdirdoesntexist'), 'Rubbish path existing on your system. Clean up!')
    def test_07(self):
        """
        Test Case 07:
        Test :py:meth:`magrathea.utils.file.File._check_file_exists` with a non-existing file.

        Test is passed if return value is True.
        """
        self.assertFalse(File._check_file_exists('/foobarstuffdirdoesntexist'))

    @skipUnless(os.path.exists('/usr/sbin'), '/usr/sbin does not exist on this system')
    def test_08(self):
        """
        Test Case 08:
        Test :py:meth:`magrathea.utils.file.File._check_file_exists` with an existing fs object not being a file.

        Test is passed if return value is False.
        """
        self.assertFalse(File._check_file_exists('/usr/sbin'))

    def test_09(self):
        """
        Test Case 09:
        Test :py:meth:`magrathea.utils.file.File._check_dir_exists` with an existing directory (this file's parent).

        Test is passed if return value is True.
        """
        self.assertTrue(File._check_dir_exists(os.path.dirname(__file__)))

    @skipIf(os.path.exists('/foobarstuffdirdoesntexist'), 'Rubbish path existing on your system. Clean up!')
    def test_10(self):
        """
        Test Case 10:
        Test :py:meth:`magrathea.utils.file.File._check_dir_exists` with a non-existing directory.

        Test is passed if return value is False.
        """
        self.assertFalse(File._check_dir_exists('/foobarstuffdirdoesntexist'))

    def test_11(self):
        """
        Test Case 11:
        Test :py:meth:`magrathea.utils.file.File._check_dir_exists` with an existing fs object not being a directory.

        Test is passed if return value is False.
        """
        self.assertFalse(File._check_dir_exists(__file__))
