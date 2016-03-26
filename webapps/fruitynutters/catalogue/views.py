from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

from fruitynutters.catalogue.models import Aisle, Item, Page, VirtualShopPage
from fruitynutters.util import get_session_cart


def info_page(request, page_name):
    """Handles text pages."""
    page_object = Page.objects.get(name__exact=page_name)
    title = page_object.title
    body = page_object.body

    response = render_to_response('info_page.html', {'title': title,
                                                     'body': body},
                                  context_instance=RequestContext(request))
    return response


def virtual_shop(request):
    """Handles virtual shop aisle."""

    page_object = VirtualShopPage.objects.get(name__exact='virtualshop')

    title = page_object.title
    body = page_object.body
    pdf_path = page_object.shopPdf.url
    last_aisle = list(Aisle.objects.filter(active=True).reverse()[:1]).pop()

    cart = get_session_cart(request.session)

    response = render_to_response('virtual_shop.html',
                                  {'cart': cart,
                                   'title': title,
                                   'body': body,
                                   'pdf_path': pdf_path,
                                   'last_aisle': last_aisle},
                                  context_instance=RequestContext(request))
    return response


def aisle_index(request):
    """Aisle list view"""

    # Get the list of active aisles.
    aisle_list = Aisle.objects.filter(active=True)

    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)

    response = render_to_response('aisle_index.html',
                                  {'aisle_list': aisle_list,
                                   'cart': cart},
                                  context_instance=RequestContext(request))
    response["Cache-Control"] = 'no-cache, no-store, must-revalidate'
    return response


def aisle(request, aisle_id):
    """Aisle detail view"""

    aisle = Aisle.objects.get(id__exact=aisle_id)
    aisle_items = \
        Item.objects.filter(aisle__exact=aisle_id).filter(active=True)

    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)

    response = render_to_response('aisle.html', {'aisle': aisle,
                                                 'aisle_items': aisle_items,
                                                 'cart': cart},
                                  context_instance=RequestContext(request))
    response["Cache-Control"] = 'no-cache, no-store, must-revalidate'
    return response


@staff_member_required
def reset_items(request):
    """Resets the new and increase/no change/decrease fields for all items."""
    all_items = Item.objects.all()

    for item in all_items:
        item.new_changed = False
        item.price_change = 'no_change'
        item.save()

    return HttpResponseRedirect('/catalogue/admin/catalogue/item/')


def aisle_mock(request):
    return render_to_response('aisle_mock.html',
                              context_instance=RequestContext(request))
