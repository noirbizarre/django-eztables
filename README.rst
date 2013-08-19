===============
Django ezTables
===============

.. image:: https://secure.travis-ci.org/noirbizarre/django-eztables.png
   :target: http://travis-ci.org/noirbizarre/django-eztables
.. image:: https://coveralls.io/repos/noirbizarre/django-eztables/badge.png?branch=master
    :target: https://coveralls.io/r/noirbizarre/django-eztables
.. image:: https://pypip.in/v/django-eztables/badge.png
    :target: https://crate.io/packages/django-eztables
.. image:: https://pypip.in/d/django-eztables/badge.png
    :target: https://crate.io/packages/django-eztables

Easy integration between jQuery DataTables and Django.

Compatibility
=============

Django ezTables requires Python 2.6+, Django 1.4+ and Django.js 0.7.6+.


Installation
============

You can install Django ezTables with pip:

.. code-block:: console

    $ pip install django-eztables

or with easy_install:

.. code-block:: console

    $ easy_install django-eztables


Add ``djangojs`` and ``eztables`` to your ``settings.INSTALLED_APPS``.

If you want to run the test suite, you will need some additionnal dependencies.
You can install them in the same time with:

.. code-block:: console

    $ pip install django-eztables[tests]


Features
========

- Datatables.net, plugins and localization integration with Django.
- Server-side processing with a simple view supporting:
    - sorting (single and multi columns)
    - filtering with regex support (global and by column)
    - formatting using format pattern
- Deferred loading support.
- Twitter Bootstrap integration.


Demo
====

You can try the demo by cloning this repository and running the test server with provided data:

.. code-block:: console

    $ python manage.py syncdb
    $ python manage.py loaddata eztables/demo/fixtures/browsers.json
    $ python manage.py runserver

Then open your browser to http://localhost:8000


Documentation
=============

The documentation is hosted `on Read the Docs <http://django-eztables.readthedocs.org/en/latest/>`_
