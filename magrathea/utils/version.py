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
    """
    Derives a `PEP 386`_ compliant version number from VERSION, assuming
    VERSION is a quintuple consisting of these elements::

       (major, minor, patch, stage, suffix)

    ``major``, ``minor``, ``patch`` and ``suffix`` are integer values, whereas ``stage``
    is a string, containing one of these key words:

    * *final* means this version is a release. In this case, ``suffix`` will be ignored.
    * *candidate* means this version is a release candidate. In this case, ``suffix`` must be
      greater than zero and indicate the ordinal numbering of the release candidate.
    * *beta* means this version is a beta release. In this case, ``suffix`` must be greater
      than zero and indicate the ordinal numbering of the beta release.
    * *alpha* means this version is either an alpha release, or a development version.
      For the first case, ``suffix`` must be greater than zero and indicate the ordinal
      numbering of the alpha release. For the latter case, ``suffix`` must be set to zero.

    The version quintuple may be passed as (only) positional argument, or as value of
    the ``version`` keyword argument. If no version quintuple is provided by argument,
    :py:data:`magrathea.VERSION` is used instead.

    .. note::

       The keyword argument overrides any positional argument. If two version quintuples are
       passed, one by positional and one by keyword argument, the one passed by keyword argument
       will win.

    :param args:   positional arguments, of which only the first one (if present) will be taken as version quintuple
    :param kwargs: keyword arguments, of which only the value of ``version`` (if present) will be taken as
                   version quintuple
    :returns: `PEP 386`_ compliant version string

    .. _PEP 386: http://www.python.org/dev/peps/pep-0386/
    """
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
    Derive the development status compliant to `PEP 301 Trove Classifiers`_ from VERSION, assuming
    VERSION is a quintuple consisting of these elements::

       (major, minor, patch, stage, suffix)

    ``major``, ``minor``, ``patch`` and ``suffix`` are integer values, whereas ``stage``
    is a string, containing one of these key words:

    * *final* means this version is a release. In this case, ``suffix`` will be ignored.
    * *candidate* means this version is a release candidate. In this case, ``suffix`` must be
      greater than zero and indicate the ordinal numbering of the release candidate.
    * *beta* means this version is a beta release. In this case, ``suffix`` must be greater
      than zero and indicate the ordinal numbering of the beta release.
    * *alpha* means this version is either an alpha release, or a development version.
      For the first case, ``suffix`` must be greater than zero and indicate the ordinal
      numbering of the alpha release. For the latter case, ``suffix`` must be set to zero.

    The version quintuple may be passed as (only) positional argument, or as value of
    the ``version`` keyword argument. If no version quintuple is provided by argument,
    :py:data:`magrathea.VERSION` is used instead.

    .. note::

       The keyword argument overrides any positional argument. If two version quintuples are
       passed, one by positional and one by keyword argument, the one passed by keyword argument
       will win.

    :param args:   positional arguments, of which only the first one (if present) will be taken as version quintuple
    :param kwargs: keyword arguments, of which only the value of ``version`` (if present) will be taken as
                   version quintuple
    :returns: Trove classifier string

    .. _PEP 301 Trove Classifiers: http://www.python.org/dev/peps/pep-0301/#distutils-trove-classification
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
    Returns a numeric identifier of the latest `Git`_ changeset.

    Since the Git revision hash does not fulfil the requirements
    of `PEP 386`_, the UTC timestamp in YYYYMMDDHHMMSS format is used
    instead. This value is not guaranteed to be unique, however the
    likeliness of collisions is small enough to be acceptable for
    the purpose of building version numbers.

    :param str path: Path to the `Git`_ repository to detect the latest commit timestamp from.
                     If not indicated, the parent path of the magrathea package is used.
    :returns: a string of the format ``GIT-timestamp`` with timestamp being either a 14 digit
              integer, or the string "unknown" in cases where the changeset timestamp could not
              be detected.

    .. _PEP 386: http://www.python.org/dev/peps/pep-0386/
    .. _Git: http://git-scm.com/
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
