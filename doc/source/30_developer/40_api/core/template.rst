Template Module
===============

.. module:: magrathea.core.template
   :synopsis: Magrathea's template module

.. py:currentmodule:: magrathea.core.template

.. note::

   This module refers to Magrathea's internal *file system templates*, not to be confused
   with Jinja2 templates.

This module manages the deployment of Magrathea's file system templates. A file system template
consists of a directory representing the template, containing by minimum a ``__init__.ini`` file.
This file must be in valid INI file syntax (as being understood by :py:mod:`configparser`), containing
at least one of ``[dirs]``, ``[files]``  and/or ``[binaries]`` sections.

**Example:**

.. code-block:: ini

   ; list of directories to be created by the template
   [dirs]
   dir1
   dir2
   dir2/dir3

   ; list of mutable files to be deployed by the template
   [files]
   dir1/file1.txt
   dir2/dir3/file2.txt

   ; list of immutable files to be deployed by the template
   [binaries]
   dir1/file1.jpg


Directories specified in the ``[dirs]`` section (usually relative to the template's root directory)
are not required to be present within the template directory; they will be created only based on the
information given in the ``__init__.ini`` file.

Files specified within the ``[files]`` section however must be present, being subject to the same
directory structure as described in ``__init__.ini``. As a special service, all files within the template's
``[file]`` section may contain Python format strings referring to any value defined in
:py:mod:`magrathea.conf.default`.

.. note::

   Since files specified within the ``[files]`` section are being processed by Python's :py:func:`format`
   function, it is highly advisable to store these file templates UTF-8 encoded, since this is the default
   encoding being used by Magrathea. Doing so will avoid painful confusion and broken characters.

Files specified within the ``[binaries]`` section will be copied without any processing. Therefore, this
section is predestined for containing binary files which shall not be modified, such as image files,
pickle or database files, etc.

.. autoclass:: magrathea.core.template.Template
   :members:
