from django.conf.urls import patterns, url

from eztables.demo.views import (
    BrowserDatatablesView,
    FormattedBrowserDatatablesView,
    CustomBrowserDatatablesView,
    SpecialCaseDatatablesView,
)

urlpatterns = patterns('',
    url(r'^$', BrowserDatatablesView.as_view(), name='browsers'),
    url(r'^formatted/$', FormattedBrowserDatatablesView.as_view(), name='formatted-browsers'),
    url(r'^custom/$', CustomBrowserDatatablesView.as_view(), name='custom-browsers'),
    url(r'^special/$', SpecialCaseDatatablesView.as_view(), name='special'),
)
