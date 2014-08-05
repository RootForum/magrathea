# -*- coding: utf-8 -*-
"""
    magrathea.utils.loader
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""

import importlib
import os
import re


def __filter_members(item):
    """
    Filter function to detect classes within a module or package

    :param str item: the item to be tested with this filter
    """
    exclude = (
        re.escape('__builtins__'),
        re.escape('__cached__'),
        re.escape('__doc__'),
        re.escape('__file__'),
        re.escape('__loader__'),
        re.escape('__name__'),
        re.escape('__package__'),
        re.escape('__path__')
    )
    pattern = re.compile('|'.join(exclude))
    return not pattern.search(item)


def __filter_modules(item):
    """
    Filter function to detect processor modules and packages

    :param str item: the item to be tested with this filter
    """
    exclude = (
        re.escape('__init__.py'),
    )
    pattern = re.compile('|'.join(exclude))
    return not pattern.search(item)


def detect_class_modules(module, parent=object):
    """
    Detect available class modules or packages and return a dictionary of valid
    class names, referring to the module they are contained within.

    :param str module: the module or package to be scanned for classes
    :param parent: the class potential candidates must be derived off
    :returns: dictionary of detected classes, mapping the class name to the module name in
              which the class has been detected
    """

    # initialise result dictionary
    result = {}
    candidates = []

    # get a list of all files and directories inside the module
    try:
        package_instance = importlib.import_module(module)
    except ImportError:
        return result

    pkg_file = os.path.splitext(package_instance.__file__)
    if pkg_file[0][-8:] == '__init__' and pkg_file[1][1:3] == 'py':
        # it's a package, so we have to look for modules
        gen_dir = os.listdir(os.path.dirname(os.path.realpath(package_instance.__file__)))

        # only consider modules and packages, and exclude the base module
        for file_candidate in filter(__filter_modules, gen_dir):

            # Python files are modules; the name needs to be without file ending
            if file_candidate[-3:] == '.py':
                file_candidate = file_candidate[:-3]

            # try if the detected package or module can be imported
            try:
                class_module_candidate = importlib.import_module('.'.join([module, file_candidate]))
            except ImportError:
                class_module_candidate = None

            # if the module or module could be imported, append it to the list of candidate modules.
            if class_module_candidate:
                candidates.append(class_module_candidate)
    else:
        candidates.append(package_instance)

    # test if any of the candidates contain
    # classes derived from the parent class
    for candidate in candidates:
        for member_candidate in filter(__filter_members, dir(candidate)):
            try:
                if issubclass(getattr(candidate, member_candidate), parent) \
                   and getattr(candidate, member_candidate).__name__ != parent.__name__:
                    result[member_candidate] = candidate.__name__
            except TypeError:
                pass

    # return the dictionary
    return result


def load_member(module, member):
    """
    Load a member (function, class, ...) from a module and return it

    :param str module: the module or package name where the class should be loaded from
    :param str member: the name of the member to be loaded
    :returns: reference to the loaded member (i. e. class or function pointer)
    """
    try:
        module = importlib.import_module(module)
    except ImportError:
        return None
    try:
        result = getattr(module, member)
    except AttributeError:
        return None
    return result
