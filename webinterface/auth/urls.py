from django.conf.urls.defaults import *

urlpatterns = patterns('webinterface.auth.views',
  (r'^$',         'main'),
  (r'^create/?$', 'create'),
  (r'^logout/?$', 'logout'),
)