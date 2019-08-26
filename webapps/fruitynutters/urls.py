from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

import fruitynutters.catalogue.views as catalogue
import fruitynutters.cart.views as cart

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += [
    url(r'^$', catalogue.info_page, {'page_name': 'index'}),
    url(r'^tips/$', catalogue.info_page, {'page_name': 'tips'}),
    url(r'^links/$', catalogue.info_page, {'page_name': 'links'}),
    url(r'^small-print/$', catalogue.info_page, {'page_name': 'small-print'}),
    url(r'^future-dates/$',
        catalogue.info_page, {'page_name': 'future-dates'}),
    url(r'^donations/$', catalogue.info_page, {'page_name': 'donations'}),

    url(r'^catalogue/$', catalogue.aisle_index),
    url(r'^catalogue/aisle/$', catalogue.aisle_index),
    url(r'^catalogue/aisle/(?P<aisle_id>\d+)/$',
        catalogue.aisle, name='aisle'),
    url(r'^catalogue/reset/$', catalogue.reset_items)
]

urlpatterns += [
    url(r'^cart/(?P<item_id>\d+)/add/$', cart.add_to_cart),
    url(r'^cart/(?P<item_id>\d+)/add/(?P<quantity>\d+)/$', cart.add_to_cart),
    url(r'^cart/addwritein/$', cart.add_writein_to_cart),
    url(r'^cart/addvirtualshopitem/$', cart.add_virtualshop_item_to_cart),
    url(r'^cart/(?P<item_id>\d+)/remove/$', cart.remove_from_cart),
    url(r'^cart/(?P<item_id>\d+)/removewritein/$',
        cart.remove_writein_from_cart),
    url(r'^cart/(?P<item_id>\d+)/removevirtualshopitem/$',
        cart.remove_virtualshop_item_from_cart),
    url(r'^cart/update/$', cart.update_cart),
    url(r'^cart/empty/$', cart.empty_cart),
    url(r'^cart/review/$', cart.review),
    url(r'^cart/submit/$', cart.submit),
    url(r'^cart/savedetails/$', cart.save_cart_details),
]

# Static mockups
urlpatterns += [
    url(r'^aislemock.html', catalogue.aisle_mock),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
