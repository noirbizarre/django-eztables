# -*- coding: utf-8 -*-
from django import forms
from django.utils.six.moves import xrange

ASC = 'asc'
DESC = 'desc'
SORT_DIRS = (
    (ASC, ASC),
    (DESC, DESC),
)


class DatatablesForm(forms.Form):
    '''
    Datatables server side processing Form

    See: http://www.datatables.net/usage/server-side
    '''
    def __init__(self, *args, **kwargs):
        super(DatatablesForm, self).__init__(*args, **kwargs)

        for idx in xrange(int(self.data['iColumns'])):
            self.fields['mDataProp_%s' % idx] = forms.CharField(required=False)
            self.fields['sSearch_%s' % idx] = forms.CharField(required=False)
            self.fields['bRegex_%s' % idx] = forms.BooleanField(required=False)
            self.fields['bSortable_%s' % idx] = forms.BooleanField(required=False)
            self.fields['bSearchable_%s' % idx] = forms.BooleanField(required=False)

        for idx in xrange(int(self.data['iSortingCols'])):
            self.fields['iSortCol_%s' % idx] = forms.IntegerField(required=True)
            self.fields['sSortDir_%s' % idx] = forms.ChoiceField(required=True, choices=SORT_DIRS)

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
