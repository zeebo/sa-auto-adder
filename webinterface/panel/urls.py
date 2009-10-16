from django.conf.urls.defaults import *

urlpatterns = patterns('webinterface.panel.views',
  (r'$^',       'panel'),
  (r'$admin/?', 'admin'),
  (r'$waves/?', 'waves'),
  (r'$queue/?', 'queue'),
)