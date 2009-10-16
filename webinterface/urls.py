from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^panel/?', include('webinterface.panel.urls')),
  (r'',        include('webinterface.auth.urls')),
)