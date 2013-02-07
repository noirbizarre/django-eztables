Server-side processing
======================


Django ezTable provide a single view to implement server-side pagination: :class:`eztables.views.DatatablesView`.

It follows the `Django Class-based Views pattern <https://docs.djangoproject.com/en/dev/topics/class-based-views/>`_ and can render Array-based or Object-based JSON.

As it extends :class:`django.views.generic.list.MultipleObjectMixin` it expects the ``model`` attribute to be set in both case.

Both modes expect a ``fields`` attribute that can optionnaly contains format patterns.

The exemple will use the same models as the demo:

.. code-block:: python

    from django.db import models


    class Engine(models.Model):
        name = models.CharField(max_length=128)
        version = models.CharField(max_length=8, blank=True)
        css_grade = models.CharField(max_length=3)

        def __unicode__(self):
            return '%s %s (%s)' % (self.name, self.version or '-', self.css_grade)


    class Browser(models.Model):
        name = models.CharField(max_length=128)
        platform = models.CharField(max_length=128)
        version = models.CharField(max_length=8, blank=True)
        engine = models.ForeignKey(Engine)

        def __unicode__(self):
            return '%s %s' % (self.name, self.version or '-')


Array-based JSON
----------------

To render an array-based JSON, you must provide ``fields`` as a  ``list`` or a ``tuple`` containing the field names.

.. code-block:: python

    from eztables.views import DatatablesView
    from myapp.models import Browser

    class BrowserDatatablesView(DatatablesView):
        model = Browser
        fields = (
            'engine__name',
            'name',
            'platform',
            'engine__version',
            'engine__css_grade',
        )


You can simply instanciate your datatable with:

.. code-block:: javascript

    $(function(){
        $('#browser-table').dataTable({
            "bPaginate": true,
            "sPaginationType": "bootstrap",
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": Django.url('dt-browsers-default')
        });
    });


Object-based JSON
-----------------

To render an array-based JSON, you must provide ``fields`` as a ``dict`` containing the mapping between the JSON fields names and the model fields.

.. code-block:: python

    from eztables.views import DatatablesView
    from myapp.models import Browser

    class ObjectBrowserDatatablesView(DatatablesView):
        model = Browser
        fields = {
            'name': 'name',
            'engine': 'engine__name',
            'platform': 'platform',
            'engine_version': 'engine__version',
            'css_grade': 'engine__css_grade',
        }


You need to use the ``aoColumns`` properties in the DataTables initialization:

.. code-block:: javascript

    $(function(){
        $('#browser-table').dataTable({
            "bPaginate": true,
            "sPaginationType": "bootstrap",
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": Django.url('dt-browsers-objects'),
            "aoColumns": [
                { "mData": "engine" },
                { "mData": "name" },
                { "mData": "platform" },
                { "mData": "engine_version" },
                { "mData": "css_grade" }
            ]
        });
    });


Format patterns
---------------

You can optionnaly provide some format patterns in the field definition:

.. code-block:: python

    from eztables.views import DatatablesView
    from myapp.models import Browser

    class FormattedBrowserDatatablesView(DatatablesView):
        model = Browser
        fields = (
            'engine__name',
            '{name} {version}',
            'platform',
            'engine__version',
            'engine__css_grade',
        )

    class FormattedObjectBrowserDatatablesView(DatatablesView):
        model = Browser
        fields = {
            'name': '{name} {version}',
            'engine': 'engine__name',
            'platform': 'platform',
            'engine_version': 'engine__version',
            'css_grade': 'engine__css_grade',
        }


Custom sort
-----------

You can implement a custom sort method.
It have to be named ``sort_col_X`` where ``X`` should be the index given by the datatables request (correspond to the filtered column).

It take the requested direction (``''`` or ``'-'``) as parameter and should return a `Django order statement <https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by>`_.

.. code-block:: python

    class CustomSortBrowserDatatablesView(BrowserDatatablesView):

        def sort_col_1(self, direction):
            '''Sort on version instead of name'''
            return '%sversion' % direction

Custom search
-------------

You can implement a custom search method.
It have to be named ``search_col_X`` where ``X`` should be the index given by the datatables request (correspond to the filtered column).

It takes the search term and the queryset to filter as parameter and should return the filtered queryset.

.. code-block:: python

    class CustomSearchBrowserDatatablesView(BrowserDatatablesView):

        def search_col_1(self, search, queryset):
            '''Search on version instead of name'''
            return queryset.filter(version__icontains=search)
