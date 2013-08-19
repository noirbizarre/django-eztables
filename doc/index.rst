.. Django ezTables documentation master file, created by
   sphinx-quickstart on Thu Feb  7 11:49:04 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django ezTables's documentation!
===========================================

Django ezTables provides easy integration between `jQuery DataTables <http://datatables.net>`_ and `Django <http://www.djangoproject.com>`_.

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

You can try the demo by cloning this repository and running the test server with the provided data:

.. code-block:: console

    $ python manage.py syncdb
    $ python manage.py loaddata eztables/demo/fixtures/browsers.json
    $ python manage.py runserver

Then open your browser to http://localhost:8000



Documentation
=============

.. toctree::
    :maxdepth: 2

    templatetags
    serverside
    localization
    integration
    api
    contribute
    changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

