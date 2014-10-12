# -*- coding: utf-8 -*-
"""
    magrathea.core.planet
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import os
import shutil
from .result import Result
from .template import Template
from ..conf import get_conf
from ..utils.compat import comp_makedirs
from ..utils.file import File
from ..utils.singleton import Singleton


@Singleton
class Planet(File):
    """
    Central Magrathea planet provider.

    This class implements all planet manipulation functionality and therefore
    serves as entry point for all kinds of user interface implementations.

    Please note that this class is decorated by the :py:class:`~magrathea.utils.singleton.Singleton`
    decorator, which means only one instance can exist. Furthermore, instances cannot
    be created directly, but must be retrieved by the ``get_instance`` method::

       planet = Planet.get_instance()

    :param str path: path on the file system where the planet resides. If not
                     specified, it defaults to the current working directory.
    """

    def __init__(self, *args, **kwargs):
        self._path = None

        if len(args) > 0:
            self._path = args[0]

        if 'path' in kwargs:
            self._path = kwargs['path']

        if not self._path:
            self._path = os.path.abspath(os.getcwd())

    def init(self, purge=True):
        """
        Initialise a new planet.

        :param bool purge: if true, remove existing content from the target directory
        """
        op_result = Result()
        op_result.merge(self._create_dir_if_not_exists(self._path, purge))
        if not op_result:
            return op_result
        template = Template(template=get_conf('PLANET_TEMPLATE'), path=self._path)
        try:
            template.deploy()
            op_result.succeed("successfully deployed template to {}".format(self._path))
        except RuntimeError as e:
            op_result.fail("Error {}".format(e))
        finally:
            return op_result

    def _create_dir_if_not_exists(self, directory='', purge=True):
        """
        Create a directory if it does not exist yet.

        :param bool purge: if true, remove existing content from the target directory
        """
        op_result = Result()
        if os.path.exists(directory):
            if os.path.isdir(directory):
                if purge:
                    try:
                        for item in os.listdir(directory):
                            if not self._check_dir_exists(item):
                                os.unlink(item)
                            else:
                                shutil.rmtree(item)
                    except OSError as e:
                        op_result.fail("Error {}".format(e))
                        return op_result
            else:
                op_result.fail("{} exists, but is not a directory".format(directory))
                return op_result
            op_result.succeed("{} already exists - no action required".format(directory))
            return op_result
        try:
            comp_makedirs(directory, exist_ok=True)
            op_result.succeed("successfully created {}".format(directory))
        except OSError as e:
            op_result.fail("Error {}".format(e))
        finally:
            return op_result
