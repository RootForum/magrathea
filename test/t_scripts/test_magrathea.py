# -*- coding: utf-8 -*-
"""
    test.t_scripts.test_magrathea
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""

try:
    import imp
    skip_imp = False
except ImportError:
    skip_imp = True

try:
    from importlib.machinery import SourceFileLoader
    skip_sf = False
except ImportError:
    skip_sf = True

import os
import sys
from unittest import TestCase, skipIf


class TestScriptsMagrathea(TestCase):
    """
    Unit tests for ``scripts/magrathea.py``
    """

    @skipIf(sys.version_info >= (3, 4, 0), "Module `imp` has been deprecated with Python 3.4")
    @skipIf(skip_imp, "Module `imp` is not available")
    def test_01_import(self):
        """
        Test Case 01:
        Try importing the magrathea script (Python<=3.3).

        Test is passed if a RuntimeError exception is raised.
        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'magrathea.py'))
        with self.assertRaises(RuntimeError):
            __ = imp.load_source('magrathea', path)

    @skipIf(sys.version_info < (3, 4, 0), "importlib has not yet replaced module `imp` in Python < 3.4")
    @skipIf(skip_sf, "Class `importlib.machinery.SourceFileLoader` is not available")
    def test_02(self):
        """
        Test Case 02:
        Try importing the magrathea script (Python>=3.4)

        Test is passed if a RuntimeError exception is raised.
        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'magrathea.py'))
        with self.assertRaises(RuntimeError):
            loader = SourceFileLoader('magrathea', path)
            __ = loader.load_module()
