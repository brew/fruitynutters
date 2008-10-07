from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden

from fruitynutters.catalogue.models import Item
from fruitynutters.cart.models import Cart, CartItem

def add_to_cart(request, item_id, quantity=1):
    if request.method == 'POST':
        quantity = int(quantity)
        cart = _get_cart_by_id(request.session.get('cart_id'))
        
        item_to_add = Item.objects.get(id__exact=item_id)
        cart.add_item(chosen_item=item_to_add, number_added=quantity)
        
        return render_to_response('cart.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})        
            
    return HttpResponseForbidden()
        
def update_cart(request):
    if request.method == "POST":
        cart = _get_cart_by_id(request.session.get('cart_id'))
        for item_id, new_quantity in request.POST.items():
            new_quantity = int(new_quantity)
            cart.update_item(item_id, new_quantity)
        
        return render_to_response('cart.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})
        
    return HttpResponseForbidden()
        
def empty_cart(request):
    if request.method == "POST":
        cart = _get_cart_by_id(request.session.get('cart_id'))
        cart.empty()
        return render_to_response('cart.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})
        
    return HttpResponseForbidden()
    
def review(request):
    """Review the current cart and collect user info."""

    # Get the cart from the session (if one exists)
    cart = _get_cart_by_id(request.session.get('cart_id'))

    return render_to_response('review.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})
    
def submit(request):
    pass

# Util 
def _get_cart_by_id(id):
    return Cart.objects.get(id__exact=id)