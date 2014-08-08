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

    def test_05(self):
        """
        Test Case 05:
        Test if the :py:class:`~magrathea.conf.ApplicationConf` class interface provides also a non-default.

        Test is passed if both, default an non-default keys exist and have the same value.
        """
        obj = ApplicationConf.get_instance()
        self.assertTrue(hasattr(obj, 'DEFAULT_CHARSET'))
        self.assertTrue(hasattr(obj, 'CHARSET'))
        self.assertEqual(obj.DEFAULT_CHARSET, obj.CHARSET)

    def test_06(self):
        """
        Test Case 06:
        Test if DEFAULT_ values really are immutable by trying to overwrite DEFAULT_CHARSET (property).

        Test is passed if :py:exc:`KeyError` is raised.
        """
        obj = ApplicationConf.get_instance()
        with self.assertRaises(KeyError):
            obj.DEFAULT_CHARSET = 'iso-8859-1'

    def test_07(self):
        """
        Test Case 07:
        Test if DEFAULT_ values really are immutable by trying to overwrite DEFAULT_CHARSET (dictionary)

        Test is passed if :py:exc:`KeyError` is raised.
        """
        obj = ApplicationConf.get_instance()
        with self.assertRaises(KeyError):
            obj['DEFAULT_CHARSET'] = 'iso-8859-1'

    def test_08(self):
        """
        Test Case 08:
        Test if DEFAULT_ values really are immutable by trying to delete DEFAULT_CHARSET (dictionary)

        Test is passed if :py:exc:`KeyError` is raised.
        """
        obj = ApplicationConf.get_instance()
        with self.assertRaises(KeyError):
            del obj['DEFAULT_CHARSET']

    def test_09(self):
        """
        Test Case 09:
        Test if non-default values are mutable by setting CHARSET (property interface).

        Test is passed if no exception is raised and CHARSET points to the new value.
        """
        obj = ApplicationConf.get_instance()
        flag = True
        try:
            obj.CHARSET = 'iso-8859-1'
        except KeyError:
            flag = False
        self.assertTrue(flag)
        self.assertEqual(obj.CHARSET, 'iso-8859-1')

    def test_10(self):
        """
        Test Case 10:
        Test if non-default values are mutable by setting CHARSET (dictionary interface).

        Test is passed if no exception is raised and CHARSET points to the new value.
        """
        obj = ApplicationConf.get_instance()
        flag = True
        try:
            obj['CHARSET'] = 'iso-8859-1'
        except KeyError:
            flag = False
        self.assertTrue(flag)
        self.assertEqual(obj['CHARSET'], 'iso-8859-1')

    def test_11(self):
        """
        Test Case 11:
        Test if non-default values can be reset by deleting them (dictionary interface).

        Test is passed if no exception is raised and CHARSET points to DEFAULT_CHARSET again.
        """
        obj = ApplicationConf.get_instance()
        flag = True
        try:
            obj['CHARSET'] = 'iso-8859-1'
            del obj['CHARSET']
        except KeyError:
            flag = False
        self.assertTrue(flag)
        self.assertEqual(obj['CHARSET'], obj['DEFAULT_CHARSET'])

    def test_12(self):
        """
        Test Case 12:
        Test if independent values can be deleted (dictionary interface).

        Test is passed if no exception is raised and member is no longer present.
        """
        obj = ApplicationConf.get_instance()
        flag = True
        try:
            obj['foo'] = 'bar'
            self.assertIn('foo', obj)
            self.assertTrue(hasattr(obj, 'foo'))
            del obj['foo']
        except KeyError:
            flag = False
        self.assertTrue(flag)
        self.assertNotIn('foo', obj)
        self.assertFalse(hasattr(obj, 'foo'))
