from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^$', 'webinterface.views.main'),
  (r'^create/?$', 'webinterface.views.create'),
  (r'^panel/?$', 'webinterface.views.panel'),
  (r'^panel/add/(?P<wave_id>.*?)/(?P<wavelet_id>.*?)/', 'webinterface.views.add_participant'),
  (r'^logout/?$', 'webinterface.views.logout'),
  
  (r'^dump/?$', 'webinterface.views.dump'),
)
