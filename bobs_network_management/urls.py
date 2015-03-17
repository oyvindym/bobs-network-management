from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('bobs_network_management.app.controlpanel.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += (
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
)
