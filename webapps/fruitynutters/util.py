from fruitynutters.cart.models import Cart

# Util
def get_session_cart(session):
    # If there is no cart id in the session, create a cart and save its id to the session.
    if not session.get('cart_id'):
        cart = Cart()
        cart.save()
        session['cart_id'] = cart.id
        return cart
    # If there is a cart id in the session try to fetch the corresponding cart.
    else:
        # Try to retrieve the cart ...
        try:
            return Cart.objects.get(id__exact=session.get('cart_id'))
        # If there's no cart matching the id, delete the id from the session and try again.
        except Cart.DoesNotExist:
            del session['cart_id']
            return get_session_cart(session)