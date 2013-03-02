.. Django ezTables documentation master file, created by
   sphinx-quickstart on Thu Feb  7 11:49:04 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django ezTables's documentation!
===========================================

Django ezTables provides easy integration between `jQuery DataTables <http://datatables.net>`_ and `Django <http://www.djangoproject.com>`_.

Compatibility
=============

Django ezTables requires Python 2.7, Django 1.4+ and Django.js 0.5+.

For Django 1.5 compatibility, you need at least Django.js 0.6.2.

Installation
============

You can install Django ezTables with pip:

.. code-block:: bash

    $ pip install django-eztables

or with easy_install:

.. code-block:: bash

    $ easy_install django-eztables


Add ``djangojs`` and ``django-eztables`` to your ``settings.INSTALLED_APPS``.


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

.. code-block:: bash

    $ python manage.py syncdb
    $ python manage.py loaddata eztables/demo/fixtures/browsers.json
    $ pyhton manage.py runserver

Then open your browser to http://localhost:8000



Documentation
=============

.. toctree::
    :maxdepth: 2

    templatetags
    serverside
    localization
    api
    changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

