from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session

from fruitynutters.catalogue.models import Item
from fruitynutters.cart.models import Cart, CartItem

def add_to_cart(request, item_id):
    if request.method == 'POST':
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.get(id__exact=cart_id)
        
        item_to_add = Item.objects.get(id__exact=item_id)
        cart.add_item(chosen_item=item_to_add, number_added=1)
        
        return render_to_response('cart.html', {'cart':cart, 'cart_items':cart.cartitem_set.all()})