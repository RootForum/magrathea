# -*- coding: utf-8 -*-
"""
    test.t_utils.test_termcolor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from unittest import TestCase
from magrathea.utils.termcolor import supports_color


class TestMagratheaUtilsTermColor(TestCase):
    """
    Unit tests for :py:mod:`magrathea.utils.termcolor`
    """

    def test_01(self):
        """
        Test Case 01:
        Test return value of :py:func:`~magrathea.utils.termcolor.supports_color`.

        Test is passed if return value is of type bool.
        """
        return_value = supports_color()
        self.assertIsInstance(return_value, bool)
