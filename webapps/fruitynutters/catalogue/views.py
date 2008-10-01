from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session

from fruitynutters.catalogue.models import Aisle, Item
from fruitynutters.cart.models import Cart

def aisle_index(request):
    
    # Get the list of aisles.
    aisle_list = Aisle.objects.all().order_by('name')
    
    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)
    
    return render_to_response('aisle_index.html', {'aisle_list':aisle_list, 'cart':cart, 'cart_items':cart.cartitem_set.all()})
    

def aisle(request, aisle_id):
    """Aisle view"""
    aisle = Aisle.objects.get(id__exact=aisle_id)
    aisle_items = Item.objects.filter(aisle__exact=aisle_id).filter(active=True).order_by('name')    
    
    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)
    
    return render_to_response('aisle.html', {'aisle':aisle, 'aisle_items':aisle_items, 'cart':cart, 'cart_items':cart.cartitem_set.all()})
    
    
def get_session_cart(session):
    # If there is no cart, create one and save its id to the session.
    if not session.get('cart_id'):
        cart = Cart()
        cart.save()
        session['cart_id'] = cart.id
        return cart
    # If there is a cart get it based on the session cart id.
    else:
        return Cart.objects.get(id__exact=session.get('cart_id'))