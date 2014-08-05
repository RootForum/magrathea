# -*- coding: utf-8 -*-
"""
    test.test_magrathea
    ~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from unittest import TestCase, skipUnless
import magrathea


class TestMagrathea(TestCase):
    """
    Unit tests for :py:mod:`magrathea`
    """

    def test_01(self):
        """
        Test Case 01:
        Test type of :py:data:`magrathea.VERSION`

        Test is passed if type of :py:data:`magrathea.VERSION` is a tuple
        """
        self.assertIsInstance(magrathea.VERSION, tuple)

    def test_02(self):
        """
        Test Case 02:
        Test length of :py:data:`magrathea.VERSION`

        Test is passed if detected length is 5
        """
        self.assertEqual(len(magrathea.VERSION), 5)

    def test_03(self):
        """
        Test Case 03:
        Test type of first member of :py:data:`magrathea.VERSION`

        Test is passed if detected type is :py:class:`int` and value is not negative
        """
        self.assertIsInstance(magrathea.VERSION[0], int)
        self.assertGreaterEqual(magrathea.VERSION[0], 0)

    def test_04(self):
        """
        Test Case 04:
        Test type of second member of :py:data:`magrathea.VERSION`

        Test is passed if detected type is :py:class:`int` and value is not negative
        """
        self.assertIsInstance(magrathea.VERSION[1], int)
        self.assertGreaterEqual(magrathea.VERSION[1], 0)

    def test_05(self):
        """
        Test Case 05:
        Test type of third member of :py:data:`magrathea.VERSION`

        Test is passed if detected type is :py:class:`int` and value is not negative
        """
        self.assertIsInstance(magrathea.VERSION[2], int)
        self.assertGreaterEqual(magrathea.VERSION[2], 0)

    def test_06(self):
        """
        Test Case 06:
        Test type of fifth member of :py:data:`magrathea.VERSION`

        Test is passed if detected type is :py:class:`int` and value is not negative
        """
        self.assertIsInstance(magrathea.VERSION[4], int)
        self.assertGreaterEqual(magrathea.VERSION[4], 0)

    def test_07(self):
        """
        Test Case 07:
        Test type of fourth member of :py:data:`magrathea.VERSION`

        Test is passed if member is one of ``alpha``, ``beta``, ``candidate``, ``final``
        """
        allowed = ('alpha', 'beta', 'candidate', 'final')
        self.assertIn(magrathea.VERSION[3], allowed)

    @skipUnless(magrathea.VERSION[3] == 'final', 'Test is only for final releases')
    def test_08(self):
        """
        Test Case 08:
        Test suffix plausibility for final releases

        Test is passed if suffix is zero.
        """
        self.assertEqual(magrathea.VERSION[4], 0)

    @skipUnless(magrathea.VERSION[3] in ('beta', 'candidate'), 'Test is only for pre-releases')
    def test_09(self):
        """
        Test Case 09:
        Test suffix plausibility for pre-releases

        Test is passed if suffix is greater than zero.
        """
        self.assertGreater(magrathea.VERSION[4], 0)

    def test_10(self):
        """
        Test Case 10:
        Test type of :py:data:`magrathea.COPYRIGHT`

        Test is passed if type of :py:data:`magrathea.COPYRIGHT` is a tuple
        """
        self.assertIsInstance(magrathea.COPYRIGHT, tuple)

    def test_11(self):
        """
        Test Case 11:
        Test length of :py:data:`magrathea.COPYRIGHT`

        Test is passed if detected length is 2
        """
        self.assertEqual(len(magrathea.COPYRIGHT), 2)

    def test_12(self):
        """
        Test Case 12:
        Test type of first member of :py:data:`magrathea.COPYRIGHT`

        Test is passed if detected type is :py:class:`str`
        """
        self.assertIsInstance(magrathea.COPYRIGHT[0], str)

    def test_13(self):
        """
        Test Case 13:
        Test type of second member of :py:data:`magrathea.COPYRIGHT`

        Test is passed if detected type is :py:class:`str`
        """
        self.assertIsInstance(magrathea.COPYRIGHT[1], str)
