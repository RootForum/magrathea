The planet.ini Configuration File
=================================

The ``planet.ini`` configuration file consists of at least one section called **DEFAULT**,
containing general configuration information regarding this planet, plus one section per
feed to be included within the planet.

.. code-block:: ini

   [DEFAULT]
   theme = default
   policy = days
   limit = 5
   paginate = 25

   [http://www.example.com/atom.xml]
   title = foo
   author = bar


DEFAULT Section
---------------

Within the default section, the following options may be specified:

.. js:data:: theme

   Name of the theme to be used when rendering the planet. The theme must exist within
   the planet's ``themes`` directory.


.. js:data:: policy

   Policy for limiting the number of feed entries to be applied when rendering the planet. May be one of

   * ``global``: limits the number of entries by simply counting them up to n (most recent first, scope:
     all feed entries).
   * ``local``: limits the number of entries by simply counting them up to n (most recent first, scope:
     entries per feed):
   * ``hours``: limits the number of entries to those published within the last n hours.
   * ``days``: limits the number of entries to those published within the last n days.
   * ``weeks``: limits the number of entries to those published within the last n weeks.
   * ``months``: limits the number of entries to those published within the last n months.
   * ``none``: does not limit the number of entries at all (not recommended)


.. js:data:: limit

   The numerical value interpreted in conjunction with the :js:data:`policy` information. With the
   :js:data:`policy` set to ``none``, this option will be ignored.


.. js:data:: paginate

   Number of entries to show per page. If the number of entries selected by :js:data:`policy` and
   :js:data:`limit` exceeds this value, the appropriate number of pages will be created.
   If set to zero, all entries will be displayed on one page.
