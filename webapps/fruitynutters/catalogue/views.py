from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

from fruitynutters.catalogue.models import Aisle, Item, Page
from fruitynutters.cart.models import Cart
from fruitynutters.util import get_session_cart

def index_page(request):
    
    index_object = InfoPage.objects.get(name__exact='index')
    title = index_object.title
    body = index_object.body
    
    response = render_to_response('info_page.html', {'title':title, 'body':body})
    return response

def aisle_index(request):
    """Aisle list view"""
    
    # Get the list of active aisles.
    aisle_list = Aisle.objects.filter(active=True).order_by('sort_name')
    
    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)
    
    response = render_to_response('aisle_index.html', {'aisle_list':aisle_list, 'cart':cart})
    response["Cache-Control"] = 'no-cache, must-revalidate'
    return response
    

def aisle(request, aisle_id):
    """Aisle detail view"""

    aisle = Aisle.objects.get(id__exact=aisle_id)
    aisle_items = Item.objects.filter(aisle__exact=aisle_id).filter(active=True).order_by('sort_name')    
    
    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)
        
    response = render_to_response('aisle.html', {'aisle':aisle, 'aisle_items':aisle_items, 'cart':cart}, context_instance=RequestContext(request))
    response["Cache-Control"] = 'no-cache, must-revalidate'
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