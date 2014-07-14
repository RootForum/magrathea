#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Magrathea - Maker of Finest Planets
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""


import os
import sys


def main():
    """
    Magrathea main function, acting as central dispatcher
    """
    # find out if running from an uninstalled version
    # this being the case, insert the appropriate path into PYTHONPATH
    magrathea_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isfile(os.path.join(magrathea_path, 'magrathea', '__init__.py')):
        sys.path.insert(0, magrathea_path)

    import magrathea.cli
    return magrathea.cli.dispatch(os.path.realpath(__file__), sys.argv)


if __name__ == '__main__':
    sys.exit(main())
else:
    raise RuntimeError("This is an executable file. Do not try to import it!")
    # noinspection PyUnreachableCode
    sys.exit(os.EX_SOFTWARE)