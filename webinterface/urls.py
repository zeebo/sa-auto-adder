from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^$', 'webinterface.views.main'),
  (r'^create/?$', 'webinterface.views.create'),
  (r'^panel/?$', 'webinterface.views.panel'),
  (r'^logout/?$', 'webinterface.views.logout'),
)
