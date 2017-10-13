Sphinx-Reload
*************

|PyPI Version| |Build Status|

.. image:: demo.gif


Installation
============

To install, use ``pip`` (or ``easy_install``):

::

    $ pip install sphinx-reload


The package installs the command-line program ``sphinx-reload``:

::

    $ sphinx-reload --version
    v0.1.0

Getting Started
===============

To begin live previewing your documentation, simply pass the path of your
documentation's root as a command-line argument with ``sphinx-reload``.
Here's an example assuming your documentation's root is under the current
directory and named ``docs``:

::

    $ sphinx-reload docs/

``sphinx-reload`` will open a preview in a new tab of your favorite browser
and watch for changes in your documentation's source
files (e.g., any `reStructuredText
<http://docutils.sourceforge.net/rst.html>`__ files under the documentation's
root).

To view further usage details, use the script's ``--help`` option:

::

    $ sphinx-reload --help

.. |Build Status| image:: https://travis-ci.org/prkumar/sphinx-reload.svg?branch=master
   :target: https://travis-ci.org/prkumar/sphinx-reload
.. |PyPI Version| image:: https://img.shields.io/pypi/v/sphinx-reload.svg
   :target: https://pypi.python.org/pypi/sphinx-reload