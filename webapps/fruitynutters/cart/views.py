from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden

from fruitynutters.catalogue.models import Item
from fruitynutters.cart.models import Cart, CartItem

def add_to_cart(request, item_id):
    if request.method == 'POST':
        cart = _get_cart_by_id(request.session.get('cart_id'))
        
        item_to_add = Item.objects.get(id__exact=item_id)
        cart.add_item(chosen_item=item_to_add, number_added=1)
        
        return render_to_response('cart.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})
    
    return HttpResponseForbidden()
        
def empty_cart(request):
    if request.method == "POST":
        cart = _get_cart_by_id(request.session.get('cart_id'))
        cart.empty()
        return render_to_response('cart.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})
        
    return HttpResponseForbidden()
        
def _get_cart_by_id(id):
    return Cart.objects.get(id__exact=id)