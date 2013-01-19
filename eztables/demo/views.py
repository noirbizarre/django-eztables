# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, ListView

from eztables.views import DatatablesView
from eztables.demo.models import Browser


class IndexView(TemplateView):
    template_name = 'eztables/index.html'


class ClientSideView(ListView):
    template_name = 'eztables/client-side.html'


class ServerSideView(TemplateView):
    template_name = 'eztables/server-side.html'


class DeferredLoadingView(TemplateView):
    template_name = 'eztables/deferred-loading.html'
    model = Browser
    context_object_name = 'browsers'


class LocalizationView(TemplateView):
    template_name = 'eztables/localization.html'


class BootstrapView(TemplateView):
    template_name = 'eztables/bootstrap.html'


class BrowserDatatablesView(DatatablesView):
    model = Browser
    fields = (
        'engine__name',
        'name',
        'platform',
        'engine__version',
        'engine__css_grade',
    )


class FormattedBrowserDatatablesView(DatatablesView):
    model = Browser
    fields = (
        'engine__name',
        '{name} {version}',
        'platform',
        'engine__version',
        'engine__css_grade',
    )
