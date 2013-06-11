from django.conf.urls import patterns, include, url

from eztables.demo.views import (
    IndexView,
    ClientSideView,
    ServerSideView,
    ServerSideSearchView,
    ServerSideObjectsView,
    ServerSideCustomView,
    DeferredLoadingView,
    LocalizationView,
    FormattedBrowserDatatablesView,
    ObjectBrowserDatatablesView,
    CustomBrowserDatatablesView,
    SpecialCaseDatatablesView,
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^client-side$', ClientSideView.as_view(), name='client-side'),
    url(r'^server-side$', ServerSideView.as_view(), name='server-side'),
    url(r'^server-side-search$', ServerSideSearchView.as_view(), name='server-side-search'),
    url(r'^server-side-objects$', ServerSideObjectsView.as_view(), name='server-side-objects'),
    url(r'^server-side-custom$', ServerSideCustomView.as_view(), name='server-side-custom'),
    url(r'^defered-loading$', DeferredLoadingView.as_view(), name='deferred-loading'),
    url(r'^localization$', LocalizationView.as_view(), name='localization'),
    url(r'^browsers/', include(patterns('',
        url(r'^default$', FormattedBrowserDatatablesView.as_view(), name='DT-browsers-default'),
        url(r'^objects$', ObjectBrowserDatatablesView.as_view(), name='DT-browsers-objects'),
        url(r'^custom$', CustomBrowserDatatablesView.as_view(), name='DT-browsers-custom'),
    ))),
    url(r'^js/', include('djangojs.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
