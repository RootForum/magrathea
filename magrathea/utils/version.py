# -*- coding: utf-8 -*-
"""
    magrathea.utils.version
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""


from magrathea.utils.convert import to_str
import magrathea
import os.path
import subprocess
import datetime


def get_version(*args, **kwargs):
    """Derives a PEP386-compliant version number from VERSION."""
    if 'version' in kwargs:
        version = kwargs['version']
    elif args:
        version = args[0]
    else:
        version = magrathea.VERSION

    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'candidate', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        git_revision = get_git_changeset()[4:]
        if git_revision != 'unknown':
            sub = '.dev{revision}'.format(revision=git_revision)
        else:
            sub = '.dev'

    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'candidate': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub


def get_development_status(*args, **kwargs):
    """
    Derive the development status compliant to `PEP301 Trove Classifiers`_ from VERSION.

    .. _PEP301 Trove Classifiers: http://www.python.org/dev/peps/pep-0301/#distutils-trove-classification

    :param tuple version: The version tuple to be used
    :return: Trove classifier string
    """
    classifiers = {
        1: 'Planning',
        2: 'Pre-Alpha',
        3: 'Alpha',
        4: 'Beta',
        5: 'Production/Stable',
        6: 'Mature',
        7: 'Inactive'
    }
    template = 'Development Status :: {number} - {Status}'
    if 'version' in kwargs:
        version = kwargs['version']
    elif args:
        version = args[0]
    else:
        version = magrathea.VERSION
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'candidate', 'final')

    agent = 1
    if version[3] == 'alpha' and version[4] == 0:
        agent = 2
    elif version[3] == 'alpha' and version[4] > 0:
        agent = 3
    elif version[3] in ('beta', 'candidate'):
        agent = 4
    elif version[3] == 'final':
        agent = 5

    return template.format(number=agent, Status=classifiers[agent])


def get_git_changeset(path=None):
    """
    Returns a numeric identifier of the latest Git changeset.

    Since the Git revision hash does not fulfil the requirements
    of PEP 386, the UTC timestamp in YYYYMMDDHHMMSS format is used
    instead. This value is not guaranteed to be unique, however the
    likeliness of collisions is small enough to be acceptable for
    the purpose of building version numbers.
    """
    if path is None:
        path = os.path.normpath(os.path.join(magrathea.__path__[0], ".."))

    # run `git show` in ControlBeast's root directory and grab its output from stdout
    git_show = subprocess.Popen(
        'git show --pretty=format:%ct --quiet HEAD',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=path,
        universal_newlines=True
    )
    try:
        timestamp = to_str(git_show.communicate()[0]).partition('\n')[0]
    except OSError:
        timestamp = None

    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except (ValueError, TypeError):
        return 'GIT-unknown'

    return 'GIT-{0:>s}'.format(timestamp.strftime('%Y%m%d%H%M%S'))
