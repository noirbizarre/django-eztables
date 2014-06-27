from django.conf.urls import patterns, url

from eztables.demo.views import (
    ObjectBrowserDatatablesView,
    FormattedObjectBrowserDatatablesView,
    CustomObjectBrowserDatatablesView,
    SpecialCaseDatatablesView,
)

urlpatterns = patterns('',
    url(r'^$', ObjectBrowserDatatablesView.as_view(), name='browsers'),
    url(r'^formatted/$', FormattedObjectBrowserDatatablesView.as_view(), name='formatted-browsers'),
    url(r'^custom/$', CustomObjectBrowserDatatablesView.as_view(), name='custom-browsers'),
    url(r'^special/$', SpecialCaseDatatablesView.as_view(), name='special'),
)
