Template tags
=============

Initialization
--------------

You can either:

- load the template tag lib into each template manually:

.. code-block:: html+django

    {% load eztables %}

- load the template tag lib by adding to your ``views.py``:

.. code-block:: python

    from django.template import add_to_builtins

    add_to_builtins('eztables.templatetags.eztables')


Usage
-----

datatables_js
~~~~~~~~~~~~~

A ``{% datatables_js %}`` tag is available to include the datatables javascript library.
After loading, you can use the Datatables library as usual:

.. code-block:: html+django

    <table id="my-table">
    </table>

    {% datatables_js %}
    <script>
        $('#my-table').dataTable();
    </script>


bootstrap support
~~~~~~~~~~~~~~~~~

If you want to use the twitter bootstrap style (based on `this blog post <http://www.datatables.net/blog/Twitter_Bootstrap_2>`_), 2 template tags are provided for:

 - ``{% datatables_bootstrap_js %}`` for the javascript part.
 - ``{% datatables_bootstrap_css %}`` for the css part.

.. code-block:: html+django

    <head>
        {% datatables_bootstrap_css %}

        {% datatables_js %}
        {% datatables_bootstrap_js %}
    </head>

    <table id="my-table">
    </table>

    <script>
        $('#my-table').dataTable({
            "bPaginate": true,
            "sPaginationType": "bootstrap",
            "bScrollCollapse": true
        });
    </script>
