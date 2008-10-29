# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.core.mail import EmailMessage

from fruitynutters.catalogue.models import Item
from fruitynutters.cart.models import Cart, CartItem
from fruitynutters.util import get_session_cart, isAddressValid
from fruitynutters.cart.order_form import createOrderForm

def add_to_cart(request, item_id, quantity=1):
    """Adds the item with item_id to the cart associated with the session."""
    if request.method == 'POST':        
        
        item_to_add = Item.objects.get(id__exact=item_id)
        cart = get_session_cart(request.session)
        # Only add active items, from active bundles.
        if not item_to_add.active or not item_to_add.aisle.active:
            request.notifications.create(Cart.CART_ITEM_UNAVAILABLE_ERROR, 'cart_error')
        else:        
            quantity = int(quantity)
            bundle = None
            # If there are items in the post request, then there are bundle items to deal with.
            # Use a list comp to create a new list containing the actual item and quantity. Only if the quantity is more than 0.
            if request.POST.items():
                bundle = [(Item.objects.get(id__exact=bi[0]), int(bi[1])) for bi in request.POST.items() if bi[1] != "" and int(bi[1]) > 0]
                request.notifications.create(Cart.CART_BUNDLE_ADDED_NOTICE, 'cart_information')
        
            cart.add_item(chosen_item=item_to_add, number_added=quantity, bundle_items=bundle)
                
        response = render_to_response('cart.html', {'cart':cart}, context_instance=RequestContext(request))
        return response
            
    return HttpResponseForbidden()
        
def update_cart(request):
    """Updates the cart associated with the session based on items in the POST object."""
    if request.method == "POST":
        cart = get_session_cart(request.session)

        items_to_update = [(Item.objects.get(id__exact=item[0]), int(item[1])) for item in request.POST.items() if item[0].isdigit()]
        for item_to_update, new_quantity in items_to_update:
            # If not a bundle, update this item.
            if not item_to_update.has_bundle:
                cart.update_item(item_to_update, new_quantity)
            else:
                request.notifications.create(Cart.CART_BUNDLE_UPDATE_WARNING, 'cart_warning')

        return render_to_response('cart.html', {'cart':cart}, context_instance=RequestContext(request))
        
    return HttpResponseForbidden()
    
def remove_from_cart(request, item_id):
    """Removes the item with item_id from the cart associated with the session."""
    if request.method == 'POST':
        cart = get_session_cart(request.session)
        cart.remove_item(item_id)
        
        response = render_to_response('cart.html', {'cart':cart}, context_instance=RequestContext(request))
        return response
        
    return HttpResponseForbidden
        
def empty_cart(request):
    """Emptys the cart object associated with the session."""
    if request.method == "POST":
        cart = get_session_cart(request.session)
        cart.empty()
        return render_to_response('cart.html', {'cart':cart}, context_instance=RequestContext(request))
        
    return HttpResponseForbidden()
    
def review(request):
    """Review the current cart and collect user info."""

    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)

    return render_to_response('review.html', {'cart':cart}, context_instance=RequestContext(request))
    

def submit(request):
    """Validates and emails the cart and member details to FNs team."""
    
    cart = get_session_cart(request.session)

    member_name = request.POST.get('member_name', '')
    member_phone = request.POST.get('member_phone', '')
    member_email = request.POST.get('member_email', '')
    order_comments = request.POST.get('order_comments', '')
    email_to_user = request.POST.get('email_member_order', False)
    
    # Validate the form and cart.
    isValid = True
    if cart.numItems == 0:
        isValid = False
        request.notifications.create("There are no items your shopping list!", 'error')
    if len(member_name) == 0:
        isValid = False
        request.notifications.create("Please enter your name", 'error')
    if len(member_phone) == 0:
        isValid = False
        request.notifications.create("Please provide a phone number in case we need to contact you", 'error')
    if len(member_email) > 0 and not isAddressValid(member_email):
        isValid = False
        request.notifications.create("Please check that your email address is valid", 'error')
    if email_to_user and len(member_email) == 0:
        isValid = False
        request.notifications.create("If you want a copy of the order sent to you, you'll need to supply your email address", 'error')


    # If it's valid, make the rtf, attach and send to the email, clear the cart and return success page.
    if isValid:
        # store the result of createOrderForm (a StringIO object) in a buffer.
        buffer = createOrderForm(cart, request.POST)
        
        email_to = ['fruitynutters@googlemail.com',]
        if email_to_user:
            email_to.append(member_email)

        # Try making and sending the email.
        try:
            mail = EmailMessage('[FruityNuttersOrder] '+member_name, 'Order attached.\n', 'specialbrew@gmail.com', email_to, headers={'Reply-To': 'fruitynutters@googlemail.com'})
            mail.attach('order_form.rtf', buffer.getvalue(), 'application/rtf')
            mail.send()
            buffer.close()
            
            # Don't need the cart anymore; empty it.
            cart.empty()
            cart.delete()
            cart.save()
            
            request.notifications.create("Your order has been submitted! Ta very much!", 'success')
        except Exception, e:
            request.notifications.create("There was a problem sending the email :( " + str(e), 'error')

        # Get the list of aisles.
        return render_to_response('review.html', {'cart':cart, 'submit_success':True}, context_instance=RequestContext(request))
    else:
        return render_to_response('review.html', {'cart':cart, 'member_name':member_name, 'member_email':member_email, 'member_phone':member_phone, 'order_comments':order_comments}, context_instance=RequestContext(request))
        

        

