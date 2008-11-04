from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session
from django.template import RequestContext

from fruitynutters.catalogue.models import Aisle, Item
from fruitynutters.cart.models import Cart
from fruitynutters.util import get_session_cart

def aisle_index(request):
    
    # Get the list of active aisles.
    aisle_list = Aisle.objects.filter(active=True).order_by('sort_name')
    
    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)
    
    response = render_to_response('aisle_index.html', {'aisle_list':aisle_list, 'cart':cart})
    response["Cache-Control"] = 'no-cache, must-revalidate'
    return response
    

def aisle(request, aisle_id):
    """Aisle view"""

    aisle = Aisle.objects.get(id__exact=aisle_id)
    aisle_items = Item.objects.filter(aisle__exact=aisle_id).filter(active=True).order_by('sort_name')    
    
    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)
        
    response = render_to_response('aisle.html', {'aisle':aisle, 'aisle_items':aisle_items, 'cart':cart}, context_instance=RequestContext(request))
    response["Cache-Control"] = 'no-cache, must-revalidate'
    return response