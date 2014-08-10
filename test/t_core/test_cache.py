# -*- coding: utf-8 -*-
"""
    test.t_core.test_cache
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import sys
import shutil
import tempfile
from unittest import TestCase, skipIf
from magrathea.core.cache import Cache

#: database name
db_name = ''


class TestMagratheaCoreCache(TestCase):
    """
    Unit tests for :py:mod:`magrathea.core.cache`
    """

    @classmethod
    def setUpClass(cls):
        global db_name
        td = tempfile.mkdtemp()
        db_name = os.path.join(td, 'cache_db')

    @classmethod
    def tearDownClass(cls):
        global db_name
        shutil.rmtree(os.path.dirname(db_name))

    def test_01(self):
        """
        Test Case 01:
        Try instantiating :py:class:`magrathea.core.cache.Cache` directly.

        Test is passed if :py:exc:`TypeError` is raised.
        """
        with self.assertRaises(TypeError):
            __ = Cache()

    @skipIf(sys.version_info < (3, 0, 0), "Singleton instance recognition only works in Python 3")
    def test_02(self):
        """
        Test Case 02:
        Try getting a :py:class:`magrathea.core.cache.Cache` via its
        :py:meth:`~magrathea.core.cache.Cache.get_instance` method

        Test is passed if instantiated object proves being a :py:class:`magrathea.core.cache.Cache` instance.
        """
        obj = Cache.get_instance()
        self.assertIsInstance(obj, Cache)

    def test_03(self):
        """
        Test Case 03:
        Test persistent data creation (dictionary interface).

        Test is passed if data persistence can be verified via both, dictionary and property interface.
        """
        global db_name
        obj1 = Cache.get_instance(db_name)
        obj1['test'] = 'test data'
        del obj1
        obj2 = Cache.get_instance(db_name)
        self.assertIn('test', obj2)
        self.assertEqual(obj2['test'], 'test data')
        self.assertTrue(hasattr(obj2, 'test'))
        self.assertEqual(obj2.test, 'test data')
        del obj2

    def test_04(self):
        """
        Test Case 04:
        Test persistent data update (dictionary interface).

        Test is passed if persistent update can be verified via both, dictionary and property interface.
        """
        global db_name
        obj1 = Cache.get_instance(db_name)
        obj1['test'] = 'test data'
        del obj1
        obj2 = Cache.get_instance(db_name)
        self.assertIn('test', obj2)
        obj2['test'] = 'other data'
        del obj2
        obj3 = Cache.get_instance(db_name)
        self.assertIn('test', obj3)
        self.assertEqual(obj3['test'], 'other data')
        self.assertTrue(hasattr(obj3, 'test'))
        self.assertEqual(obj3.test, 'other data')
        del obj3

    def test_05(self):
        """
        Test Case 05:
        Test persistent data delete (dictionary interface)

        Test is passed if persistent delete can be verified by both, dictionary and property interface.
        """
        global db_name
        obj1 = Cache.get_instance(db_name)
        obj1['test'] = 'test data'
        del obj1
        obj2 = Cache.get_instance(db_name)
        self.assertIn('test', obj2)
        del obj2['test']
        self.assertNotIn('test', obj2)
        del obj2
        obj3 = Cache.get_instance(db_name)
        self.assertNotIn('test', obj3)
        self.assertFalse(hasattr(obj3, 'test'))
        del obj3
