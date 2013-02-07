Localization
============


Django ezTable embed DataTables localizations.

Thay have the following naming convention::

    {{STATIC_URL}}/js/libs/datatables/language.{{LANG}}.json

You can simply retrieve them with django.js_:

.. code-block:: javascript

    $('#my-table').dataTable({
        ...
        "oLanguage": {
            "sUrl": Django.file("js/libs/datatables/language.fr.json")
        }
        ...
    });

You can obtain the current language code with django.js_ too:

.. code-block:: javascript

    var code = Django.context.LANGUAGE_CODE;

Be carefull, no localization is provided for English language.


.. _django.js: http://pypi.python.org/pypi/django.js
