# -*- coding: utf-8 -*-
"""
    test.t_scripts.test_magrathea
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""

import imp
import os
from unittest import TestCase


class Test_scripts_magrathea(TestCase):
    """
    Unit tests for ``scripts/magrathea.py``
    """

    def test_01_import(self):
        """
        Test 01: importing the magrathea script should be prohibited
        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'magrathea.py'))
        with self.assertRaises(RuntimeError):
            __ = imp.load_source('magrathea', path)
