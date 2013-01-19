# -*- coding: utf-8 -*-
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.views.generic.list import MultipleObjectMixin

from eztables.forms import DatatablesForm, ASC, DESC


JSON_MIMETYPE = 'application/json'


class RowAdapter(object):
    '''
    Base row adapter class

    Row adapter allow custom row processing before serialization.
    '''
    def __init__(self, rows):
        self.rows = rows

    def get_rows(self):
        return [self.get_row(row) for row in self.rows]

    def get_row(self, row):
        raise NotImplemented


class DefaultRowAdapter(RowAdapter):
    '''
    The default row adapter.

    Simply get all the fields.
    '''
    def get_row(self, row):
        return list(row)


class DatatablesView(MultipleObjectMixin, View):
    '''
    Render a paginated server-side Datatables JSON view.

    See: http://www.datatables.net/usage/server-side
    '''
    fields = []
    adapter_class = DefaultRowAdapter

    def post(self, request, *args, **kwargs):
        return self.process_response(request.POST)

    def get(self, request, *args, **kwargs):
        return self.process_response(request.GET)

    def process_response(self, data):
        self.form = DatatablesForm(data)
        if self.form.is_valid():
            self.object_list = self.get_queryset().values_list(*self.fields)
            return self.render_to_response(self.form)
        else:
            return HttpResponseBadRequest()

    def get_queryset(self):
        qs = super(DatatablesView, self).get_queryset()
        iSortingCols = self.form.cleaned_data['iSortingCols']
        orders_idx = [self.form.cleaned_data['iSortCol_%s' % i] for i in xrange(iSortingCols)]
        orders_dirs = [self.form.cleaned_data['sSortDir_%s' % i] for i in xrange(iSortingCols)]
        orders = map(lambda i, d: '%s%s' % ('-' if d == DESC else '', self.fields[i]), orders_idx, orders_dirs)
        return qs.order_by(*orders)

    def get_page(self, form):
        page_size = form.cleaned_data['iDisplayLength']
        start_index = form.cleaned_data['iDisplayStart']
        paginator = Paginator(self.object_list, page_size)
        num_page = (start_index / page_size) + 1
        return paginator.page(num_page)

    def render_to_response(self, form, **kwargs):
        page = self.get_page(form)
        data = {
            'iTotalRecords': page.paginator.count,
            'iTotalDisplayRecords': page.paginator.count,
            'sEcho': form.cleaned_data['sEcho'],
            'aaData': self.adapter_class(page.object_list).get_rows(),
        }
        return self.json_response(data)

    def json_response(self, data):
        return HttpResponse(
            json.dumps(data, cls=DjangoJSONEncoder),
            mimetype=JSON_MIMETYPE
        )
