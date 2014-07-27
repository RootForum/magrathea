# -*- coding: utf-8 -*-
"""
    test.t_utils.test_version
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from unittest import TestCase
from magrathea.utils.version import get_version, get_development_status


class TestMagratheaUtilsVersion(TestCase):
    """
    Unit tests for :py:mod:`magrathea.utils.version`
    """

    def test_01(self):
        """
        Test Case 01:
        Test :py:func:`~magrathea.utils.version.get_version` with a release version without patch level.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 0, 'final', 0)
        result = get_version(version=version)
        self.assertEqual(result, '0.1')

    def test_02(self):
        """
        Test Case 02:
        Test :py:func:`~magrathea.utils.version.get_version` with a release version with patch level.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 1, 'final', 0)
        result = get_version(version=version)
        self.assertEqual(result, '0.1.1')

    def test_03(self):
        """
        Test Case 03:
        Test :py:func:`~magrathea.utils.version.get_version` with an alpha version without suffix.

        Test is passed if returned result meets expected string pattern
        """
        version = (0, 1, 0, 'alpha', 0)
        result = get_version(version=version)
        self.assertRegexpMatches(result, r'^0\.1\.dev\d{14}$')

    def test_04(self):
        """
        Test Case 04:
        Test :py:func:`~magrathea.utils.version.get_version` with an alpha version with suffix.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 0, 'alpha', 1)
        result = get_version(version=version)
        self.assertEqual(result, '0.1a1')

    def test_05(self):
        """
        Test Case 05:
        Test :py:func:`~magrathea.utils.version.get_version` with an beta version with suffix.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 0, 'beta', 1)
        result = get_version(version=version)
        self.assertEqual(result, '0.1b1')

    def test_06(self):
        """
        Test Case 06:
        Test :py:func:`~magrathea.utils.version.get_version` with an rc version with suffix.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 0, 'rc', 1)
        result = get_version(version=version)
        self.assertEqual(result, '0.1c1')

    def test_07(self):
        """
        Test Case 07:
        Test :py:func:`~magrathea.utils.version.get_version` with a too short version tuple.

        Test is passed if :py:exc:`AssertionError` is raised
        """
        version = (0, 1, 0, 'final')
        with self.assertRaises(AssertionError):
            get_version(version=version)

    def test_08(self):
        """
        Test Case 08:
        Test :py:func:`~magrathea.utils.version.get_version` with a too long version tuple.

        Test is passed if :py:exc:`AssertionError` is raised
        """
        version = (0, 1, 0, 'final', 0, 1)
        with self.assertRaises(AssertionError):
            get_version(version=version)

    def test_09(self):
        """
        Test Case 09:
        Test :py:func:`~magrathea.utils.version.get_version` with an invalid version status designator.

        Test is passed if :py:exc:`AssertionError` is raised
        """
        version = (0, 1, 0, 'release', 0)
        with self.assertRaises(AssertionError):
            get_version(version=version)

    def test_10(self):
        """
        Test Case 10:
        Test :py:func:`~magrathea.utils.version.get_development_status` with a release version without patch level.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 0, 'final', 0)
        result = get_development_status(version=version)
        self.assertEqual(result, 'Development Status :: 5 - Production/Stable')

    def test_11(self):
        """
        Test Case 11:
        Test :py:func:`~magrathea.utils.version.get_development_status` with a release version with patch level.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 1, 'final', 0)
        result = get_development_status(version=version)
        self.assertEqual(result, 'Development Status :: 5 - Production/Stable')

    def test_12(self):
        """
        Test Case 12:
        Test :py:func:`~magrathea.utils.version.get_development_status` with an alpha version without suffix.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 0, 'alpha', 0)
        result = get_development_status(version=version)
        self.assertEqual(result, 'Development Status :: 2 - Pre-Alpha')

    def test_13(self):
        """
        Test Case 13:
        Test :py:func:`~magrathea.utils.version.get_development_status` with an alpha version with suffix.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 0, 'alpha', 1)
        result = get_development_status(version=version)
        self.assertEqual(result, 'Development Status :: 3 - Alpha')

    def test_14(self):
        """
        Test Case 14:
        Test :py:func:`~magrathea.utils.version.get_development_status` with a beta version with suffix.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 0, 'beta', 1)
        result = get_development_status(version=version)
        self.assertEqual(result, 'Development Status :: 4 - Beta')

    def test_15(self):
        """
        Test Case 15:
        Test :py:func:`~magrathea.utils.version.get_development_status` with an rc version with suffix.

        Test is passed if returned result meets expected string
        """
        version = (0, 1, 0, 'rc', 1)
        result = get_development_status(version=version)
        self.assertEqual(result, 'Development Status :: 4 - Beta')

    def test_16(self):
        """
        Test Case 16:
        Test :py:func:`~magrathea.utils.version.get_development_status` with a too short version tuple.

        Test is passed if :py:exc:`AssertionError` is raised
        """
        version = (0, 1, 0, 'final')
        with self.assertRaises(AssertionError):
            get_development_status(version=version)

    def test_17(self):
        """
        Test Case 17:
        Test :py:func:`~magrathea.utils.version.get_development_status` with a too long version tuple.

        Test is passed if :py:exc:`AssertionError` is raised
        """
        version = (0, 1, 0, 'final', 0, 1)
        with self.assertRaises(AssertionError):
            get_development_status(version=version)

    def test_18(self):
        """
        Test Case 18:
        Test :py:func:`~magrathea.utils.version.get_development_status` with an invalid version status designator.

        Test is passed if :py:exc:`AssertionError` is raised
        """
        version = (0, 1, 0, 'release', 0)
        with self.assertRaises(AssertionError):
            get_development_status(version=version)
