from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^catalogue/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^catalogue/admin/(.*)', admin.site.root),
)

urlpatterns += patterns('fruitynutters.catalogue.views',
    (r'^catalogue/aisle/$', 'aisle_index'),
    (r'^catalogue/aisle/(?P<aisle_id>\d+)/$', 'aisle'),
)

urlpatterns += patterns('fruitynutters.cart.views',
    (r'^cart/(?P<item_id>\d+)/add/$', 'add_to_cart'),
    (r'^cart/(?P<item_id>\d+)/add/(?P<quantity>\d+)/$', 'add_to_cart'),
    (r'^cart/update/$', 'update_cart'),
    (r'^cart/empty/$', 'empty_cart'),
    (r'^cart/review/$', 'review'),
    (r'^cart/submit/$', 'submit'),
)