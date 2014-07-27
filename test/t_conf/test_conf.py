# -*- coding: utf-8 -*-
"""
    test.t_conf.test_conf
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from unittest import TestCase
from magrathea.conf import get_conf, ApplicationConf


class TestMagratheaConf(TestCase):
    """
    Unit tests for :py:mod:`magrathea.conf`
    """

    def test_01(self):
        """
        Test Case 01:
        Test :py:mod:`magrathea.conf` via the :py:func:`~magrathea.conf.get_conf` function interface (valid key).

        Test is passed if returned value corresponds to expected value.
        """
        key = 'DEFAULT_CHARSET'
        result = get_conf(key)
        self.assertEqual(result, 'utf-8')

    def test_02(self):
        """
        Test Case 02:
        Test :py:mod:`magrathea.conf` via the :py:func:`~magrathea.conf.get_conf` function interface (invalid key).

        Test is passed if returned value is None.
        """
        key = 'TEST_TEST_TEST'
        result = get_conf(key)
        self.assertIsNone(result)

    def test_03(self):
        """
        Test Case 03:
        Test the :py:class:`~magrathea.conf.ApplicationConf` class interface via property interface.

        Test is passed if expected property is found and has the right value.
        """
        obj = ApplicationConf.get_instance()
        self.assertTrue(hasattr(obj, 'DEFAULT_CHARSET'))
        self.assertEqual(obj.DEFAULT_CHARSET, 'utf-8')

    def test_04(self):
        """
        Test Case 04:
        Test the :py:class:`~magrathea.conf.ApplicationConf` class interface via dictionary interface.

        Test is passed if expected key is found and has the right value.
        """
        obj = ApplicationConf.get_instance()
        self.assertIn('DEFAULT_CHARSET', obj)
        self.assertEqual(obj['DEFAULT_CHARSET'], 'utf-8')
