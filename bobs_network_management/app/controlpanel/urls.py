from django.conf.urls import patterns, url

urlpatterns = patterns('bobs_network_management.app.controlpanel.views',
	url(r'^$', 'controlpanel', name='controlpanel'),
)