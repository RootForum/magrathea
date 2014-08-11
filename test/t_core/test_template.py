# -*- coding: utf-8 -*-
"""
    test.t_core.test_template
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import shutil
import tempfile
from unittest import TestCase, skipUnless, skipIf
from magrathea.conf import get_conf, ApplicationConf
from magrathea.core.template import Template
from magrathea.utils.compat import CompConfigParser, comp_open


class TestMagratheaCoreTemplate(TestCase):
    """
    Unit tests for :py:mod:`magrathea.core.template`
    """

    def test_01(self):
        """
        Test Case 01:
        Try creating an instance of :py:class:`magrathea.core.template.Template`.

        Test is passed if instance proves being an instance of :py:class:`magrathea.core.template.Template`.
        """
        obj = Template()
        self.assertIsInstance(obj, Template)

    def test_02(self):
        """
        Test Case 02:
        Try setting :py:meth:`magrathea.core.template.Template.path` to an existing, writable path.

        Test is passed if :py:meth:`magrathea.core.template.Template.path` points to this path.
        """
        name = tempfile.mkdtemp()
        obj = Template()
        obj.path = name
        self.assertEqual(name, obj.path)
        shutil.rmtree(name)

    @skipUnless(os.path.exists('/usr/sbin'), '/usr/sbin does not exist on this system')
    def test_03(self):
        """
        Test Case 03:
        Try setting :py:meth:`magrathea.core.template.Template.path` to an existing, non-writable path.

        Test is passed if :py:meth:`magrathea.core.template.Template.path` points to its previous value.
        """
        obj = Template()
        name = obj.path
        obj.path = '/usr/sbin'
        self.assertEqual(obj.path, name)

    @skipIf(os.path.exists('/foobarstuffdirdoesntexist'), 'Rubbish path existing on your system. Clean up!')
    def test_04(self):
        """
        Test Case 04:
        Try setting :py:meth:`magrathea.core.template.Template.path` to a non-existing path.

        Test is passed if :py:meth:`magrathea.core.template.Template.path` points to its previous value.
        """
        obj = Template()
        name = obj.path
        obj.path = '/foobarstuffdirdoesntexist'
        self.assertEqual(obj.path, name)

    def test_05(self):
        """
        Test Case 05:
        Try setting :py:meth:`magrathea.core.template.Template.template` to an existing template.

        Test is passed if :py:meth:`magrathea.core.template.Template.template` points to this template.
        """
        obj = Template()
        obj.template = 'planet'
        self.assertEqual(obj.template, 'planet')

    def test_06(self):
        """
        Test Case 06:
        Try setting :py:meth:`magrathea.core.template.Template.template` to a non-existing template.

        Test is passed if :py:meth:`magrathea.core.template.Template.template` points to its previous value.
        """
        obj = Template()
        name = obj.template
        obj.template = 'foo'
        self.assertEqual(obj.template, name)

    def test_07(self):
        """
        Test Case 07:
        Deploy a template into a temporary directory.

        Test is passed if deployment doesn't raise exception and all expected files exist.
        """
        def _filter(item):
            _file_map = {
                'makefile': 'Makefile',
                'cmakelists.txt': 'CMakeLists.txt',
                'readme': 'README'
            }
            if item in _file_map:
                return _file_map[item]
            return item

        td = tempfile.mkdtemp()
        obj = Template(template='planet', path=td)
        obj.deploy()
        cp = CompConfigParser(allow_no_value=True)
        cf = ApplicationConf.get_instance()
        with comp_open(os.path.join(get_conf('DEFAULT_TEMPLATE_PATH'), 'planet', '__init__.ini'), mode='r') as fp:
            content = fp.read()
            content = content.format(**cf)
        cp.read_string(content)
        flag = True
        if cp.has_section('dirs'):
            for directory in cp.options('dirs'):
                flag = flag and os.path.exists(os.path.join(obj.path, directory))
        if cp.has_section('files'):
            for file in cp.options('files'):
                flag = flag and os.path.exists(os.path.join(obj.path, _filter(file)))
        if cp.has_section('binaries'):
            for binary in cp.options('binaries'):
                flag = flag and os.path.exists(os.path.join(obj.path, _filter(binary)))
        shutil.rmtree(td)
        self.assertTrue(flag)
