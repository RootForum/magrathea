Version Numbering
=================

Magrathea's versions are numbered in a `PEP 386`_ compliant scheme. Internally,
versions are represented by a quintuple consisting of these elements::

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

**Example**::

   >>> import magrathea
   >>> magrathea.VERSION
   (0, 1, 0, 'alpha', 0)
   >>> magrathea.get_version()
   '0.1.dev20140803095419'

This representation scheme ensures version tuples can easily be compared by using normal
Python comparison operators (``<``, ``>``, ``=`` and their combinations)::

   >>> import magrathea
   >>> magrathea.VERSION
   (0, 1, 0, 'alpha', 0)
   >>> magrathea.VERSION > (0, 1, 0, 'final', 0)
   False


Main Version
------------

The main version (or release version) is indicated only by the major and minor version
numbers. Thus, all versions starting with the same major and minor version numbers belong
to the same main version.


Releases
--------

Release versions are labelled with a version number using either the
``major.minor.patch`` scheme, or (for cases where the patch level
corresponds to zero) the ``major.minor`` scheme.

Greater numbers mean more recent versions; however since the ranking is done
first by the major version, then by the minor version and last by the patch
level, a version comparison does not necessarily allow conclusions regarding
the release date.

**Examples:**

* *1.0* is a valid version
* *1.0.1* is also a valid version, referring to a more recent patch level
* *1.0.0* is **not** a valid version; it would be written as *1.0*


Release Candidates
------------------

Release candidates follow the same scheme as releases, but bear a suffix marking
them as release candidates. Usually, the to-be release is suffixed by ``c`` and
a number (greater than zero) indicating the order of this release candidate within
all release candidates for the specific version.

**Examples:**

* *1.0c1* is the first release candidate for version *1.0*
* *1.0c* is an invalid version information (the suffixed candidate counter is missing)
* *1.0c0* is also an invalid version label (cf. preceding case)


Beta Versions
-------------

Beta versions designate pre-release versions made available for public testing before
they are mature enough for becoming release candidates. Beta releases are marked by
a suffix consisting of the letter ``b`` and a number (greater than zero) indicating the
order of this beta release within all beta releases for this specific version.

**Examples:**

* *1.0b1* is the first beta of version *1.0*
* *1.0b* is an invalid version information (the suffixed beta counter is missing)
* *1.0b0* is also an invalid label (cf. preceding case)


Alpha Versions
--------------

Alpha versions designate pre-release versions made available for public testing before
they are mature enough for becoming beta versions. Alpha releases are marked by a suffix
consisting of the letter ``a`` and a number (greater than zero) indicating the order of
this alpha release within all alpha releases for this specific version.

**Examples:**

* *1.0a1* is the first alpha of version *1.0*
* *1.0a* is an invalid version information (the suffixed alpha counter is missing)
* *1.0a0* is also an invalid label (cf. preceding case)


Development Versions
--------------------

Before entering the pre-release stage, Magrathea versions are designated by the future
to be version number, suffixed by ``dev`` and a fourteen digits number indicating the
time stamp (``YYYYmmddHHMMSS``) of the Git commit this current version is based on. If
the Git revision is unknown or cannot be detected, the numeric part of the suffix may
be left out.

**Example:**

* *0.1.dev20140803095419* designates the version represented by the ``master`` tree as
  committed on *August 3, 2014 09:54:19 UTC*
* *0.1.dev* designates a version represented by the ``master`` tree somewhere before it
  entered the pre-release stage for version *0.1*

.. _PEP 386: http://www.python.org/dev/peps/pep-0386/
