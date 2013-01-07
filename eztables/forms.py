# -*- coding: utf-8 -*-
from django import forms


class DatatablesForm(forms.Form):
    '''
    Datatables server side processing Form

    See: http://www.datatables.net/usage/server-side
    '''
    #: Display start point in the current data set.
    iDisplayStart = forms.IntegerField()

    #: Number of records that the table can display in the current draw.
    #: It is expected that the number of records returned will be equal to this number,
    #: unless the server has fewer records to return.
    iDisplayLength = forms.IntegerField()

    #: Number of columns being displayed (useful for getting individual column search info)
    iColumns = forms.IntegerField()

    #: Global search field
    sSearch = forms.CharField(required=False)

    #: True if the global filter should be treated as a regular expression for advanced filtering, false if not.
    bRegex = forms.BooleanField(required=False)

    #: Number of columns to sort on
    iSortingCols = forms.IntegerField()

    #: Information for DataTables to use for rendering.
    sEcho = forms.CharField()
