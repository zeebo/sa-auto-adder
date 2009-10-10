from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r"^$", "sa_auto_adder.main.views.main"),
    (r"^login/$", "sa_auto_adder.main.views.login"),
    (r'^panel/$', "sa_auto_adder.main.views.panel"),
    (r'^create/$', "sa_auto_adder.main.views.create"),
    # Example:
    # (r'^sa_auto_adder/', include('sa_auto_adder.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
)
