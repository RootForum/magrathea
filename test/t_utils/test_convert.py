## -*- coding: utf-8 -*-
"""
    test.t_utils.test_convert
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
from unittest import TestCase
from magrathea.utils.convert import to_bytes, to_str


class TestConvert(TestCase):
    """
    Unit tests for :py:mod:`magrathea.utils.convert`
    """

    def test_01(self):
        """
        Test Case 01:
        Convert a non-empty string to bytes.

        Test is passed if the returned result is a byte sequence and equals the expected result.
        """
        test_string = "test"
        test_bytes = b"test"
        self.assertIsInstance(to_bytes(test_string), bytes)
        self.assertSequenceEqual(to_bytes(test_string), test_bytes)

    def test_02(self):
        """
        Test Case 02:
        Convert an empty string to bytes.

        Test is passed if the returned result is a byte sequence and equals the expected result.
        """
        test_string = ""
        test_bytes = b""
        self.assertIsInstance(to_bytes(test_string), bytes)
        self.assertSequenceEqual(to_bytes(test_string), test_bytes)

    def test_03(self):
        """
        Test Case 03:
        Convert a byte sequence to bytes.

        Test is passed if the returned result is a byte sequence and equals the expected result.
        """
        test_string = bytes(b"test")
        test_bytes = b"test"
        self.assertIsInstance(to_bytes(test_string), bytes)
        self.assertSequenceEqual(to_bytes(test_string), test_bytes)

    def test_04(self):
        """
        Test Case 04:
        Convert a byte array to bytes.

        Test is passed if the returned result is a byte sequence and equals the expected result.
        """
        test_string = bytearray(b"test")
        test_bytes = b"test"
        self.assertIsInstance(to_bytes(test_string), bytes)
        self.assertSequenceEqual(to_bytes(test_string), test_bytes)

    def test_05(self):
        """
        Test Case 05:
        Convert None to bytes.

        Test is passed if the returned result is a byte sequence and equals the expected result.
        """
        test_string = None
        test_bytes = b""
        self.assertIsInstance(to_bytes(test_string), bytes)
        self.assertSequenceEqual(to_bytes(test_string), test_bytes)

    def test_06(self):
        """
        Test Case 06:
        Convert False to bytes.

        Test is passed if the returned result is a byte sequence and equals the expected result.
        """
        test_string = False
        test_bytes = b"False"
        self.assertIsInstance(to_bytes(test_string), bytes)
        self.assertSequenceEqual(to_bytes(test_string), test_bytes)

    def test_07(self):
        """
        Test Case 07:
        Convert a non-string object to bytes.

        Test is passed if the returned result is a byte sequence and equals the expected result.
        """
        test_string = [1, 2, 3]
        test_bytes = b"[1, 2, 3]"
        self.assertIsInstance(to_bytes(test_string), bytes)
        self.assertSequenceEqual(to_bytes(test_string), test_bytes)

    def test_08(self):
        """
        Test Case 08:
        Convert a non-empty byte sequence into a string.

        Test is passed if the returned result is a string and equals the expected result.
        """
        test_string = "test"
        test_bytes = b"test"
        self.assertIsInstance(to_str(test_bytes), str)
        self.assertSequenceEqual(to_str(test_bytes), test_string)

    def test_09(self):
        """
        Test Case 09:
        Convert an empty byte sequence into a string.

        Test is passed if the returned result is a sting and equals the expected result.
        """
        test_string = ""
        test_bytes = b""
        self.assertIsInstance(to_str(test_bytes), str)
        self.assertSequenceEqual(to_str(test_bytes), test_string)

    def test_10(self):
        """
        Test Case 10:
        Convert a byte sequence into a string.

        Test is passed if the returned result is a string and equals the expected result.
        """
        test_string = "test"
        test_bytes = bytes(b"test")
        self.assertIsInstance(to_str(test_bytes), str)
        self.assertSequenceEqual(to_str(test_bytes), test_string)

    def test_11(self):
        """
        Test Case 11:
        Convert a byte array into a string.

        Test is passed if the returned result is a string and equals the expected result.
        """
        test_string = "test"
        test_bytes = bytearray(b"test")
        self.assertIsInstance(to_str(test_bytes), str)
        self.assertSequenceEqual(to_str(test_bytes), test_string)

    def test_12(self):
        """
        Test Case 12:
        Convert None into a string.

        Test is passed if the returned result is a string and equals the expected result.
        """
        test_string = ""
        test_bytes = None
        self.assertIsInstance(to_str(test_bytes), str)
        self.assertSequenceEqual(to_str(test_bytes), test_string)

    def test_13(self):
        """
        Test Case 13:
        Convert False into a string.

        Test is passed if the returned result is a string and equals the expected result.
        """
        test_string = "False"
        test_bytes = False
        self.assertIsInstance(to_str(test_bytes), str)
        self.assertSequenceEqual(to_str(test_bytes), test_string)

    def test_14(self):
        """
        Test Case 14:
        Convert a non-bytes object into a string.

        Test is passed if the returned result is a string and equals the expected result.
        """
        test_string = "[1, 2, 3]"
        test_bytes = [1, 2, 3]
        self.assertIsInstance(to_str(test_bytes), str)
        self.assertSequenceEqual(to_str(test_bytes), test_string)
