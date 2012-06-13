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


# Ported from Recipe 3.9 in Secure Programming Cookbook for C and C++ by
# John Viega and Matt Messier (O'Reilly 2003)
from string import *
rfc822_specials = '()<>@,;:\\"[]'


def isAddressValid(addr):
    # First we validate the name portion (name@domain)
    c = 0
    while c < len(addr):
        if addr[c] == '"' and (not c or addr[c - 1] == '.' or addr[c - 1] == '"'):
            c = c + 1
            while c < len(addr):
                if addr[c] == '"': break
                if addr[c] == '\\' and addr[c + 1] == ' ':
                    c = c + 2
                    continue
                if ord(addr[c]) < 32 or ord(addr[c]) >= 127: return 0
                c = c + 1
            else: return 0
            if addr[c] == '@': break
            if addr[c] != '.': return 0
            c = c + 1
            continue
        if addr[c] == '@': break
        if ord(addr[c]) <= 32 or ord(addr[c]) >= 127: return 0
        if addr[c] in rfc822_specials: return 0
        c = c + 1
    if not c or addr[c - 1] == '.': return 0

    # Next we validate the domain portion (name@domain)
    domain = c = c + 1
    if domain >= len(addr): return 0
    count = 0
    while c < len(addr):
        if addr[c] == '.':
            if c == domain or addr[c - 1] == '.': return 0
            count = count + 1
        if ord(addr[c]) <= 32 or ord(addr[c]) >= 127: return 0
        if addr[c] in rfc822_specials: return 0
        c = c + 1

    return count >= 1
