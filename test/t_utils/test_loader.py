# -*- coding: utf-8 -*-
"""
    test.t_utils.test_loader
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import sys
import shutil
import tempfile
from unittest import TestCase
from magrathea.utils.loader import detect_class_modules, load_member


test_package = [
    """from argparse import ArgumentParser

class TestOne(ArgumentParser):
    pass
""",
    """from argparse import ArgumentParser

class TestTwo(ArgumentParser):
    pass
""",
    """from argparse import HelpFormatter

class TestThree(HelpFormatter):
    pass
"""
]

test_module = """from argparse import ArgumentParser, HelpFormatter

class TestOne(ArgumentParser):
    pass

class TestTwo(ArgumentParser):
    pass

class TestThree(HelpFormatter):
    pass
"""


def construct_package(name, path):
    """
    Construct a package with the given name at the location specified by path.

    :param str name: name of the package to construct
    :param str path: path where to construct the package
    """
    package_path = os.path.join(path, name)
    os.makedirs(package_path)
    fp = open(os.path.join(package_path, '__init__.py'), 'w')
    fp.close()
    for i in range(0, 3, 1):
        fp = open(os.path.join(package_path, 'test_module{}.py'.format(i)), 'w')
        fp.write(test_package[i])
        fp.close()


def construct_module(name, path):
    """
    Construct a module with the given name at the location specified by path.

    :param str name: name of the module to construct
    :param str path: path where to construct the module
    """
    fp = open(os.path.join(path, name+'.py'), 'w')
    fp.write(test_module)
    fp.close()


class TestMagratheaUtilsLoader(TestCase):
    """
    Unit tests for :py:mod:`magrathea.utils.loader`

    .. note::

       Instead of the more modern temporary directory construction using the
       :py:class:`tempfile.TemporaryDirectory` context manager, the traditional
       method is used here for the sake of backward compatibility to Python 2.7.

    """

    def test_01(self):
        """
        Test Case 01:
        Detect existing classes in an existing artificial package test environment.

        Test is passed if the returned dictionary matches with the expected result.
        """
        expected = {
            'TestOne': 'loader_test01.test_module0',
            'TestTwo': 'loader_test01.test_module1'
        }
        from argparse import ArgumentParser
        td = tempfile.mkdtemp()
        construct_package('loader_test01', td)
        sys.path.insert(0, td)
        result = detect_class_modules('loader_test01', ArgumentParser)
        sys.path.remove(td)
        shutil.rmtree(td)
        self.assertDictEqual(expected, result)

    def test_02(self):
        """
        Test Case 02:
        Detect existing classes in an existing artificial module test environment.

        Test is passed if the returned dictionary matches with the expected result.
        """
        expected = {
            'TestOne': 'loader_test02',
            'TestTwo': 'loader_test02'
        }
        from argparse import ArgumentParser
        td = tempfile.mkdtemp()
        construct_module('loader_test02', td)
        sys.path.insert(0, td)
        result = detect_class_modules('loader_test02', ArgumentParser)
        sys.path.remove(td)
        shutil.rmtree(td)
        self.assertDictEqual(expected, result)

    def test_03(self):
        """
        Test Case 03:
        Detect non-existing classes in an existing artificial package test environment.

        Test is passed if the returned dictionary matches with the expected result.
        """
        expected = {}
        td = tempfile.mkdtemp()
        construct_package('loader_test03', td)
        sys.path.insert(0, td)
        result = detect_class_modules('loader_test03', TestCase)
        sys.path.remove(td)
        shutil.rmtree(td)
        self.assertDictEqual(expected, result)

    def test_04(self):
        """
        Test Case 04:
        Detect non-existing classes in a non-existing test environment.

        Test is passed if the returned dictionary matches with the expected result.
        """
        expected = {}
        result = detect_class_modules('this_hopefully_does_not_exist', TestCase)
        self.assertDictEqual(expected, result)

    def test_05(self):
        """
        Test Case 05:
        Load class from artificial test environment.

        Test is passed if loaded class can be instantiated, proving its own identity.
        """
        from argparse import ArgumentParser
        td = tempfile.mkdtemp()
        construct_package('loader_test05', td)
        sys.path.insert(0, td)
        loaded = load_member('loader_test05.test_module1', 'TestTwo')
        sys.path.remove(td)
        shutil.rmtree(td)
        obj = loaded()
        self.assertIsInstance(obj, ArgumentParser)
