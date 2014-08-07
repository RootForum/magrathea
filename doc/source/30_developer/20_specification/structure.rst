Magrathea Planet Directory Structure
====================================

Each planet built and maintained by Magrathea is stored within a dedicated directory.
By convention, this directory will contain the following elements:

* ``planet.ini`` -- configuration file for the planet
* ``cache.db`` -- persistent cache representation (may have a different file suffix)
* ``themes/`` -- directory containing custom themes
* ``build/`` -- directory containing the built planet

Usually, when initialising a planet using Magrathea's command line interface, the
presence of all four required elements will be ensured.
