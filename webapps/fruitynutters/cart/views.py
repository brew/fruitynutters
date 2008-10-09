from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden

from fruitynutters.catalogue.models import Item
from fruitynutters.cart.models import Cart, CartItem
from fruitynutters.util import get_session_cart

def add_to_cart(request, item_id, quantity=1):
    if request.method == 'POST':
        quantity = int(quantity)
        cart = get_session_cart(request.session)

        # Code here for testing whether there are bundle items and adding them to the cart.

        bundle = None
        # If there are items in the post request, then there are bundle items to deal with.
        # Use a list comp to create a new list containing the actual item and quantity. Only if the quantity is more than 0.
        if request.POST.items():
            bundle = [(Item.objects.get(id__exact=bi[0]), int(bi[1])) for bi in request.POST.items() if int(bi[1]) > 0]
        
        item_to_add = Item.objects.get(id__exact=item_id)
        cart.add_item(chosen_item=item_to_add, number_added=quantity, bundle_items=bundle)
        
        return render_to_response('cart.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})        
            
    return HttpResponseForbidden()
        
def update_cart(request):
    if request.method == "POST":
        cart = get_session_cart(request.session)
        for item_id, new_quantity in request.POST.items():
            new_quantity = int(new_quantity)
            cart.update_item(item_id, new_quantity)
        
        return render_to_response('cart.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})
        
    return HttpResponseForbidden()
        
def empty_cart(request):
    if request.method == "POST":
        cart = get_session_cart(request.session)
        cart.empty()
        return render_to_response('cart.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})
        
    return HttpResponseForbidden()
    
def review(request):
    """Review the current cart and collect user info."""

    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)

    return render_to_response('review.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})
    
def submit(request):
    pass
