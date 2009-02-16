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
    (r'^$', 'info_page', {'page_name':'index'}),
    (r'^tips/$', 'info_page', {'page_name':'tips'}),
    (r'^links/$', 'info_page', {'page_name':'links'}),
    (r'^small-print/$', 'info_page', {'page_name':'small-print'}),
    (r'^future-dates/$', 'info_page', {'page_name':'future-dates'}),
    (r'^donations/$', 'info_page', {'page_name':'donations'}),
    
    (r'^catalogue/$', 'aisle_index'),
    (r'^catalogue/aisle/$', 'aisle_index'),
    (r'^catalogue/aisle/(?P<aisle_id>\d+)/$', 'aisle'),
    (r'^catalogue/reset/$', 'reset_items'),
    (r'^catalogue/virtualshop/$', 'virtual_shop'),
)

urlpatterns += patterns('fruitynutters.cart.views',
    (r'^cart/(?P<item_id>\d+)/add/$', 'add_to_cart'),
    (r'^cart/(?P<item_id>\d+)/add/(?P<quantity>\d+)/$', 'add_to_cart'),
    (r'^cart/addwritein/$', 'add_writein_to_cart'),
    (r'^cart/addvirtualshopitem/$', 'add_virtualshop_item_to_cart'),
    (r'^cart/(?P<item_id>\d+)/remove/$', 'remove_from_cart'),
    (r'^cart/(?P<item_id>\d+)/removewritein/$', 'remove_writein_from_cart'),
    (r'^cart/(?P<item_id>\d+)/removevirtualshopitem/$', 'remove_virtualshop_item_from_cart'),
    (r'^cart/update/$', 'update_cart'),
    (r'^cart/empty/$', 'empty_cart'),
    (r'^cart/review/$', 'review'),
    (r'^cart/submit/$', 'submit'),
    (r'^cart/savedetails/$', 'save_cart_details'),
)

# Static mockups
urlpatterns += patterns('fruitynutters.catalogue.views', 
    (r'^aislemock.html', 'aisle_mock'),
)