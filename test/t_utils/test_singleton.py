# -*- coding: utf-8 -*-
"""
    test.t_utils.test_singleton
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from unittest import TestCase
from magrathea.utils.singleton import Singleton


@Singleton
class OldStyleClassWithoutArgs:
    """Old style class with an argument-free constructor"""


@Singleton
class OldStyleClassWithArgs:
    """Old style class with constructor expecting arguments"""

    def __init__(self, *args, **kwargs):
        self.test = None
        if len(args) > 0:
            self.test = args[0]
        if 'test' in kwargs:
            self.test = kwargs['test']


@Singleton
class NewStyleClassWithoutArgs(object):
    """New style class with an argument-free constructor"""
    pass


@Singleton
class NewStyleClassWithArgs(object):
    """New style class with constructor expecting arguments"""

    def __init__(self, *args, **kwargs):
        self.test = None
        if len(args) > 0:
            self.test = args[0]
        if 'test' in kwargs:
            self.test = kwargs['test']


class TestMagratheaUtilsSingleton(TestCase):
    """
    Unit tests for :py:mod:`magrathea.utils.singleton`
    """

    def test_01(self):
        """
        Test Case 01:
        Try instantiating directly a decorated old-style class without arguments.

        Test is passed if a :py:exc:`TypeError` exception is raised.
        """
        with self.assertRaises(TypeError):
            obj = OldStyleClassWithoutArgs()

    def test_02(self):
        """
        Test Case 02:
        Try instantiating directly a decorated new-style class without arguments.

        Test is passed if a :py:exc:`TypeError` exception is raised.
        """
        with self.assertRaises(TypeError):
            obj = NewStyleClassWithoutArgs()

    def test_03(self):
        """
        Test Case 03:
        Try instantiating directly a decorated old-style class with arguments.

        Test is passed if a :py:exc:`TypeError` exception is raised.
        """
        with self.assertRaises(TypeError):
            obj = OldStyleClassWithArgs(test='foo')

    def test_04(self):
        """
        Test Case 04:
        Try instantiating directly a decorated new-style class with arguments.

        Test is passed if a :py:exc:`TypeError` exception is raised.
        """
        with self.assertRaises(TypeError):
            obj = NewStyleClassWithArgs(test='foo')

    def test_05(self):
        """
        Test Case 05:
        Try getting two instance references of a decorated old-style class without arguments.

        Test is passed if both references identify the same object.
        """
        obj1 = OldStyleClassWithoutArgs.get_instance()
        obj2 = OldStyleClassWithoutArgs.get_instance()
        self.assertEqual(id(obj1), id(obj2))

    def test_06(self):
        """
        Test Case 06:
        Try getting two instance references of a decorated new-style class without arguments.

        Test is passed if both references identify the same object.
        """
        obj1 = NewStyleClassWithoutArgs.get_instance()
        obj2 = NewStyleClassWithoutArgs.get_instance()
        self.assertEqual(id(obj1), id(obj2))

    def test_07(self):
        """
        Test Case 07:
        Try getting two instance references of a decorated old-style class with arguments.

        Test is passed if both references identify the same object.
        """
        obj1 = OldStyleClassWithArgs.get_instance(test='foo')
        obj2 = OldStyleClassWithArgs.get_instance()
        self.assertEqual(id(obj1), id(obj2))

    def test_08(self):
        """
        Test Case 08:
        Try getting two instance references of a decorated new-style class with arguments.

        Test is passed if both references identify the same object.
        """
        obj1 = NewStyleClassWithArgs.get_instance(test='foo')
        obj2 = NewStyleClassWithArgs.get_instance()
        self.assertEqual(id(obj1), id(obj2))

    def test_09(self):
        """
        Test Case 09:
        Try overriding a property of a decorated old-style class with arguments.

        Test is passed if first property setting is kept unchanged.
        """
        obj1 = OldStyleClassWithArgs.get_instance(test='foo')
        obj2 = OldStyleClassWithArgs.get_instance(test='bar')
        self.assertEqual(obj2.test, 'foo')

    def test_10(self):
        """
        Test Case 10:
        Try overriding a property of a decorated new-style class with arguments.

        Test is passed if first property setting is kept unchanged.
        """
        obj1 = NewStyleClassWithArgs.get_instance(test='foo')
        obj2 = NewStyleClassWithArgs.get_instance(test='bar')
        self.assertEqual(obj2.test, 'foo')
