Release Management
==================

Release Philosophy
------------------

Here is a bunch of rules which roughly describes what Magrathea's version philosophy looks like:

* Minor version switches usually indicate a new feature
* Major version switches usually indicate a breach of backwards compatibility
* With a new major version, usually previous major version lines become deprecated, which means that
  no new features will be developed for these major version lines.
* Main versions still being supported will however still be subject to security and errata fixes, even
  if their major version has been declared deprecated.
* Releases having been followed by a patch release are obsolete and will be considered as outdated and
  maybe even harmful. Do never use such a retired release!


Release Lifecycle
-----------------

#. Usually, the lifecycle of a release begins in a *development* stage.
#. Once all features scheduled for a main version have been implemented, the release moves forward
   to the *alpha* stage.
#. Once the alpha stage has been passed (meaning the code is no longer to be considered harmful),
   the release may pass forward to the *beta* stage.
#. Once the public bug hunting has been finished and a stable behaviour has been reported on all
   targeted platforms, the release will be promoted to the *release candidate* stage.
#. If no bugs are reported by the wider field of public testers, the release candidate will be
   promoted to a *final release* of a main version.
#. Should a security flaw or other error be detected for the already released version, an appropriate
   *patch release* will be provided (depending on its size and complexity, this may happen without
   any or just a limited subset of the previously described pre-release stages).
#. Releases which have become obsolete by newer releases will at some point in time be *retired*, i. e.
   they will no longer be supported, and security flaws will no longer be fixed.


Development Stage
-----------------

The development stage takes place in the ``master`` branch of the blessed repository. Preferably,
the development of dedicated new features shall happen in cloned repositories and then be merged
into the ``master`` branch via the pull request mechanism.

The development stage is concluded by a feature freeze, meaning no new features shall be merged into
the ``master`` branch.


Pre-Release Stage
-----------------

The general pre-release stage (alpha and beta stages) takes place in the feature-frozen ``master``
branch of the blessed repository. During this stage, pull requests with new features will be postponed
until the feature freeze will be released.

Intermediate versions being published as alpha or beta releases shall be tagged with an appropriate
label, corresponding to the correct version string.

The pre-release stage is concluded by being ready for the first release candidate.


Release Stage
-------------

The release stage takes place in a dedicated ``releng`` branch. The branch is created from the ``master``
branch once the beta stage is considered as concluded. Creation of the ``releng`` branch automatically
releases the feature freeze for the ``master`` branch.

Intermediate versions being published as release candidates up to the final release shall be tagged with
an appropriate label, corresponding to the correct version string.

The release stage is concluded by creating and publishing the final main version release.


Maintenance Stage
-----------------

The maintenance stage takes place within the corresponding ``releng`` branch *after* the final main
version has been released. During this stage, only bug fixes shall be applied to the ``releng`` branch.

Versions being published as patch release for the corresponding main version release shall be tagged with
an appropriate label, corresponding to the correct version string.

The maintenance stage is concluded by retiring the main version the ``releng`` branch was created for.
Retired branches may be archived within a separate repository and removed from the blessed repository,
particularly if the blessed repository is getting too big and non-performing.
