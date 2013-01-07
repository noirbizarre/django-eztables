from django.conf.urls import patterns, include, url

from eztables.demo.views import (
    IndexView,
    ClientSideView,
    ServerSideView,
    DeferredLoadingView,
    LocalizationView,
    BootstrapView,
    AdaptedBrowserDatatablesView,
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^client-side$', ClientSideView.as_view(), name='client-side'),
    url(r'^server-side$', ServerSideView.as_view(), name='server-side'),
    url(r'^defered-loading$', DeferredLoadingView.as_view(), name='deferred-loading'),
    url(r'^boostrap$', BootstrapView.as_view(), name='bootstrap'),
    url(r'^localization$', LocalizationView.as_view(), name='localization'),
    url(r'^datatables$', AdaptedBrowserDatatablesView.as_view(), name='browsers-datatables'),
    url(r'^js/', include('djangojs.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
