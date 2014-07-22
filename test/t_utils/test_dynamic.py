# -*- coding: utf-8 -*-
"""
    test.t_utils.test_dynamic
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from unittest import TestCase
from magrathea.utils.dynamic import Dynamic, DynamicIterable


class TestMagratheaUtilsDynamic(TestCase):
    """
    Unit tests for :py:mod:`magrathea.utils.dynamic`
    """

    def test_01(self):
        """
        Test Case 01:
        Try instantiating a Dynamic object.

        Test is passed if the instance proves being a :py:class:`~magrathea.utils.dynamic.Dynamic` instance.
        """
        obj = Dynamic()
        self.assertIsInstance(obj, Dynamic)

    def test_02(self):
        """
        Test Case 02:
        Instantiate a dynamic object with payload data.

        Test is passed if the corresponding attribute can be verified
        """
        d = {'test': 123}
        obj = Dynamic(**d)
        self.assertTrue(hasattr(obj, 'test'))

    def test_03(self):
        """
        Test Case 03:
        Try instantiating a DynamicIterable object.

        Test is passed if the instance proves being a :py:class:`~magrathea.utils.dynamic.DynamicIterable` instance.
        """
        obj = DynamicIterable()
        self.assertIsInstance(obj, DynamicIterable)

    def test_04(self):
        """
        Test Case 04:
        Insert data into a DynamicIterable object and verify dictionary-style accessibility.

        Test is passed if the added member is in the keys and the linked data equal to the inserted test data.
        """
        obj = DynamicIterable()
        obj['test'] = 123
        self.assertIn('test', obj)
        self.assertEqual(obj['test'], 123)

    def test_05(self):
        """
        Test Case 05:
        Insert data into a DynamicIterable object and verify object-style accessibility.

        Test is passed if the object proves having a corresponding attribute, providing the inserted test data.
        """
        obj = DynamicIterable()
        obj['test'] = 123
        self.assertTrue(hasattr(obj, 'test'))
        self.assertEqual(obj.test, 123)

    def test_06(self):
        """
        Test Case 06:
        Create a DynamicIterable with initial data passed as dictionary.

        Test is passed if initial member is in the keys and the linked data is equal to the initial test data.
        """
        d = {'test': 123}
        obj = DynamicIterable(d)
        self.assertIn('test', obj)
        self.assertEqual(obj['test'], 123)

    def test_07(self):
        """
        Test Case 07:
        Create a DynamicIterable with initial data passed as keyword arguments.

        Test is passed if initial member is in the keys and the linked data is equal to the initial test data.
        """
        d = {'test': 123}
        obj = DynamicIterable(**d)
        self.assertIn('test', obj)
        self.assertEqual(obj['test'], 123)

    def test_08(self):
        """
        Test Case 08:
        Delete data from a DynamicIterable object after having added it.

        Test is passed if initially added attribute, key and data have disappeared.
        """
        d = {'test': 123}
        obj = DynamicIterable(d)
        del obj['test']
        self.assertNotIn('test', obj)
        self.assertFalse(hasattr(obj, 'test'))

    def test_09(self):
        """
        Test Case 09:
        Verify dictionary behaviour of DynamicIterable by initialising it with a dictionary.

        Test is passed if a dictionary comparison with the initialisation dictionary succeeds.
        """
        d = {'test': 123}
        obj = DynamicIterable(d)
        self.assertTrue(d == obj)
