# -*- coding: utf-8 -*-
"""
    magrathea.core.template
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import shutil
from ..conf import get_conf, ApplicationConf
from ..utils.file import File
from ..utils.compat import comp_makedirs, comp_open, CompConfigParser


class Template(File):
    """
    Template Manager Object.

    The Template Object can be used to deploy Magrathea templates to
    a specific location on the file system.

    A Magrathea template consists at least of the template's root directory,
    containing a file named ``__init__.ini``. This file is expected to be in valid
    INI file syntax, describing the template's content.

    At least one of the ``dirs``, ``files`` or ``binaries`` sections must be present; otherwise nothing
    will be deployed. The file templates described in the ``files`` section must be present within
    the template's directory, mirroring the described directory structure. Taking the above-given
    example, the template file ``file1.txt`` must be located within ``dir1`` in the template's root
    directory.

    All template files, including ``__init__.ini`` may use Python format strings with designators
    defined in :py:mod:`magrathea.conf.default`.

    :param str template:    name of the template to work with
    :param str path:        destination for the template deployment
    """

    #: Name of the template to work with
    _template = None

    #: Path to deploy to
    _path = None

    #: Dictionary constructed form the template's __init__.ini
    _ini = None

    def __init__(self, template='', path=None):
        """
        Template Object constructor
        """
        self.template = template
        if not path:
            self.path = os.path.abspath(os.getcwd())
        else:
            self.path = os.path.abspath(path)

    @property
    def path(self):
        """
        Path to deploy the template to.
        Expected to be a string representing a valid path name with write access.
        """
        return self._path

    @path.setter
    def path(self, path):
        if self._check_path(path):
            self._path = path

    @property
    def template(self):
        """
        Name of the ControlBeast Template to work with.
        Expected to be a string representing a valid template name.
        """
        return self._template

    @template.setter
    def template(self, template):
        if self._check_template_name(template):
            self._template = template

    def deploy(self):
        """
        Deploy the template onto the file system.
        """
        if not self._ini:
            self._load_template()
        if not self._ini:
            raise RuntimeError('Could not load template. __init__.ini missing or damaged.')
        if 'dirs' in self._ini:
            for dirname in self._ini['dirs']:
                comp_makedirs(os.path.join(self._path, dirname), exist_ok=True)
        if 'files' in self._ini:
            conf = ApplicationConf.get_instance()
            for filename in self._ini['files']:
                with comp_open(
                        os.path.join(get_conf('DEFAULT_TEMPLATE_PATH'), self._template, filename),
                        mode='r'
                ) as fp:
                    content = fp.read()
                    content = content.format(**conf)
                    with comp_open(os.path.join(self._path, filename), mode='w') as wp:
                        wp.write(content)
        if 'binaries' in self._ini:
            for filename in self._ini['binaries']:
                shutil.copy2(
                    os.path.join(get_conf('DEFAULT_TEMPLATE_PATH'), self._template, filename),
                    os.path.join(self._path, filename)
                )

    def _check_path(self, path):
        """
        Check whether the given path exists and if yes, if it's writeable.

        :param str path:    Name of the path to be tested
        :return:            True if the path can be used for deployment, False if not
        :rtype:             bool
        """
        result = False
        if self._check_dir_exists(path):
            # ok, path is an existing file system object and a directory. But is it also writeable?
            if self._check_access(os.path.abspath(path), os.W_OK):
                # Perfect.
                result = True
        else:
            # hm, the path doesn't exist. but could we create it? let's find the last existing parent...
            parent = os.path.dirname(os.path.abspath(path))
            while not self._check_dir_exists(parent):
                parent = os.path.dirname(parent)
            if self._check_access(os.path.abspath(parent), os.W_OK):
                # good news, we could create the path
                result = True
        return result

    def _check_template_name(self, template):
        """
        Check whether the given template name is an existing ControlBeast template and can be accessed.

        :param str template:    Name of the template to be verified
        :return:                True if the template is valid, False if not
        :rtype:                 bool
        """
        filename = os.path.join(get_conf('DEFAULT_TEMPLATE_PATH'), template, '__init__.ini')
        if self._check_file_exists(filename) and self._check_access(filename, os.R_OK):
            return True
        else:
            return False

    def _load_template(self):
        """
        Load the template information from the template's ``__init__.ini``
        """
        filename = os.path.join(get_conf('DEFAULT_TEMPLATE_PATH'), self._template, '__init__.ini')
        cf = ApplicationConf.get_instance()
        with comp_open(filename, mode='r') as fp:
            content = fp.read()
            content = content.format(**cf)
        conf = CompConfigParser(allow_no_value=True)
        conf.read_string(content, '__init__.ini')
        ini = {'dirs': [], 'files': [], 'binaries': []}
        if conf.has_section('dirs'):
            for key in conf.options('dirs'):
                ini['dirs'].append(key)
        if conf.has_section('files'):
            for key in conf.options('files'):
                ini['files'].append(key)
        if conf.has_section('binaries'):
            for key in conf.options('binaries'):
                ini['binaries'].append(key)
        if isinstance(self._ini, dict):
            self._ini.update(ini)
        else:
            self._ini = ini
