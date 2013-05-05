# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, ListView

from eztables.views import DatatablesView
from eztables.demo.models import Browser, SpecialCase


class IndexView(TemplateView):
    template_name = 'eztables/index.html'


class ClientSideView(ListView):
    template_name = 'eztables/client-side.html'
    model = Browser
    context_object_name = 'browsers'


class ServerSideView(TemplateView):
    template_name = 'eztables/server-side-base.html'


class ServerSideSearchView(TemplateView):
    template_name = 'eztables/server-side-search.html'


class ServerSideObjectsView(TemplateView):
    template_name = 'eztables/server-side-objects.html'


class ServerSideCustomView(TemplateView):
    template_name = 'eztables/server-side-custom.html'


class DeferredLoadingView(TemplateView):
    template_name = 'eztables/deferred-loading.html'
    model = Browser
    context_object_name = 'browsers'


class LocalizationView(TemplateView):
    template_name = 'eztables/localization.html'


class BrowserDatatablesView(DatatablesView):
    model = Browser
    fields = (
        'engine__name',
        'name',
        'version',
        'platform',
        'engine__version',
        'engine__css_grade',
    )


class FormattedBrowserDatatablesView(DatatablesView):
    model = Browser
    fields = (
        'engine__name',
        '{name} {version}',
        'version',
        'platform',
        'engine__version',
        'engine__css_grade',
    )


class ObjectBrowserDatatablesView(DatatablesView):
    model = Browser
    fields = {
        'name': 'name',
        'engine': 'engine__name',
        'version': 'version',
        'platform': 'platform',
        'engine_version': 'engine__version',
        'css_grade': 'engine__css_grade',
    }


class FormattedObjectBrowserDatatablesView(DatatablesView):
    model = Browser
    fields = {
        'name': '{name} {version}',
        'version': 'version',
        'engine': 'engine__name',
        'platform': 'platform',
        'engine_version': 'engine__version',
        'css_grade': 'engine__css_grade',
    }


class CustomSearchSort(object):

    def sort_col_1(self, direction):
        '''Sort on version instead of name'''
        return '%sversion' % direction

    def sort_col_3(self, direction):
        '''Sort on name and platform instead of platform'''
        return ('%sname' % direction, '%splatform' % direction)

    def search_col_1(self, search, queryset):
        '''Search on version instead of name'''
        return queryset.filter(version__icontains=search)


class CustomBrowserDatatablesView(CustomSearchSort, BrowserDatatablesView):
    pass


class CustomObjectBrowserDatatablesView(CustomSearchSort, ObjectBrowserDatatablesView):
    pass


class SpecialCaseDatatablesView(DatatablesView):
    model = SpecialCase
    fields = (
        'big_integer_field',
        'boolean_field',
        'char_field',
        'comma_separated_integer_field',
        'date_field',
        'datetime_field',
        'decimal_field',
        'email_field',
        'email_field',
        'file_field',
        'file_path_field',
        'float_field',
        'generic_ip_address_field',
        'image_field',
        'integer_field',
        'ip_address_field',
        'null_boolean_field',
        'positive_integer_field',
        'positive_small_integer_field',
        'slug_field',
        'small_integer_field',
        'text_field',
        'text_field',
        'time_field',
        'url_field',
    )
