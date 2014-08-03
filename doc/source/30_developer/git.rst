Version Control
===============

Source Code Management
----------------------

Magrathea uses `Git`_ as its SCM. The project's "blessed" Git repository resides at `GitHub`_. It is publicly
accessible, but only core maintainers can push into this blessed repository.


Repository Structure
--------------------

Within the blessed `repository`_, a number of branches exist which are dedicated to a specific purpose:

* ``master`` is the main development branch and contains the code for the next release
* ``releng_xx_yy`` branches contain the code of the release designated by xx.yy (where x is the major version, and
  y the minor version, both displayed as two-digit number).
* ``feature_xyz`` branches are used for the development of features. Their names are always prefixed by ``feature_``,
  followed by a Git branch name compliant slug describing the feature.


Master Branch
-------------

The master branch is meant to contain code for the next Magrathea main version. This covers
development versions and parts of the pre-release stages. Therefore, strictness with the code
quality may vary with the progress towards a release. However, as a common minimum requirement,
each commit done to the blessed repository's ``master`` branch must contain only working code,
which in particular means:

* The code is covered by unit tests
* All unit tests run without error and green result
* Code and corresponding unit tests are documented (at least the API documentation is available)
* The code does not contain any FIXME tags
* The code may however still contain TODO tags


Release Engineering Branches
----------------------------

For each Magrathea main version, a corresponding ``releng`` branch exists. These branches are meant
to only contain production-quality code (candidate and final releases). After a main version has been
released, only bug fixes (security and errata fixes) shall be applied to these branches, and only if
they are intended to be released as a patch or bug fixing release.


Feature Branches
----------------

For the implementation and testing of new features, separate feature branches shall be used. Usually,
development of new features does not take place within the blessed repository, but in a clone. Once
the feature is mature enough for making its way into the master branch of the blessed repository,
a pull request shall be opened to notify the maintainers of the blessed repository.


.. _Git: http://git-scm.com/
.. _GitHub: https://github.com/RootForum/magrathea
.. _repository: https://github.com/RootForum/magrathea
.. _Sphinx: http://sphinx-doc.org
.. _Travis CI: https://travis-ci.org/daemotron/controlbeast
