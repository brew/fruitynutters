# -*- coding: utf-8 -*-

import logging
from smtplib import SMTPException

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt

from fruitynutters.settings import (ORDER_FORM_SEND_EMAIL,
                                    ORDER_FORM_REPLY_TO_EMAIL)
from fruitynutters.catalogue.models import Item
from fruitynutters.cart.models import Cart
from fruitynutters.util import get_session_cart, isAddressValid
from fruitynutters.cart.order_form import createOrderForm

log = logging.getLogger('cart')


@csrf_exempt
def add_to_cart(request, item_id, quantity=1):
    """Add the item with item_id to the cart associated with the session."""
    if request.method == 'POST':

        item_to_add = Item.objects.get(id__exact=item_id)
        cart = get_session_cart(request.session)
        # Only add active items, from active aisles.
        if not item_to_add.active or not item_to_add.aisle.active:
            request.notifications.create(Cart.CART_ITEM_UNAVAILABLE_ERROR,
                                         'cart_error')
        else:
            quantity = int(request.POST.get('quantity', quantity))

            bundle = None
            # If there are bundle items in the post request, create a new list
            # containing the actual item and quantity, if the quantity is more
            # than 0.
            if request.POST.get('has_bundle', False):
                bundle = [(Item.objects.get(id__exact=i[0].split(':')[1]),
                           int(i[1]))
                          for i in request.POST.items()
                          if i[0].startswith('bi:') and
                          i[1] != '' and int(i[1]) > 0]
                request.notifications.create(Cart.CART_BUNDLE_ADDED_NOTICE,
                                             'cart_information')

            cart.add_item(chosen_item=item_to_add, number_added=quantity,
                          bundle_items=bundle)
            cart.remove_multiple_cart_item(chosen_item_id=item_to_add.id)

        if request.is_ajax():
            response = render_to_response(
                'cart.html', {'cart': cart},
                context_instance=RequestContext(request))
        else:
            response = redirect(request.POST.get('next', '/'))
        return response

    return HttpResponseForbidden()


@csrf_exempt
def add_writein_to_cart(request):
    """Adds a write-in item to the cart associated with the session."""
    if request.method == "POST":
        cart = get_session_cart(request.session)

        description = request.POST.get('writein_description', '')
        code = request.POST.get('writein_code', '')

        isValid = True
        if len(description) == 0:
            isValid = False
            request.notifications.create("Please add a description.",
                                         'writein_error')
        if len(code) == 0:
            isValid = False
            request.notifications.create("Please add a product code.",
                                         'writein_error')

        show_writein = "False"
        if isValid is True:
            # Form is valid, process it here!
            cart.add_writein_item(name=description, code=code)

            # Now the form is processed, finish up with the data.
            description = ''
            code = ''

        show_writein = "True"

        return render_to_response(
            'cart.html', {'cart': cart,
                          'writein_description': description,
                          'writein_code': code,
                          'show_writein': show_writein},
            context_instance=RequestContext(request))

    return HttpResponseForbidden()


@csrf_exempt
def add_virtualshop_item_to_cart(request):
    """Adds a virtual shop item to the cart associated with the session."""
    if request.method == "POST":
        cart = get_session_cart(request.session)

        description = request.POST.get('virtualshop_description', '')
        quantity = request.POST.get('virtualshop_quantity', '')

        isValid = True
        if len(description) == 0:
            isValid = False
            request.notifications.create("Please add a description.",
                                         'cart_error')
        if len(quantity) == 0:
            isValid = False
            request.notifications.create("Please add a quantity.",
                                         'cart_error')

        if isValid is True:
            try:
                quantity = int(quantity)
            except ValueError:
                request.notifications.create("Quantity must be a number.",
                                             'cart_error')
                return render_to_response(
                    'cart.html', {'cart': cart},
                    context_instance=RequestContext(request))

            cart.add_virtualshop_item(name=description, quantity=quantity)

        return render_to_response(
            'cart.html', {'cart': cart},
            context_instance=RequestContext(request))

    return HttpResponseForbidden()


@csrf_exempt
def update_cart(request):
    """Updates the cart associated with the session based on items in the POST
    object."""
    if request.method == "POST":
        cart = get_session_cart(request.session)

        try:
            items_to_update = \
                [(Item.objects.get(id__exact=item[0]), int(item[1]))
                 for item in request.POST.items() if item[0].isdigit()]
        except ValueError:
            request.notifications.create(Cart.CART_INVALID_UPDATE_NUMBER_ERROR,
                                         'cart_error')
            return render_to_response(
                'cart.html', {'cart': cart},
                context_instance=RequestContext(request))

        for item_to_update, new_quantity in items_to_update:
            # If not a bundle, update this item.
            if not item_to_update.has_bundle:
                cart.update_item(item_to_update, new_quantity)
            else:
                request.notifications.create(Cart.CART_BUNDLE_UPDATE_WARNING,
                                             'cart_warning')

        return render_to_response(
            'cart.html', {'cart': cart},
            context_instance=RequestContext(request))

    return HttpResponseForbidden()


@csrf_exempt
def remove_from_cart(request, item_id):
    """Removes the item with item_id from the cart associated with the
    session."""
    if request.method == 'POST':
        cart = get_session_cart(request.session)
        cart.remove_item(item_id)

        response = render_to_response(
            'cart.html', {'cart': cart},
            context_instance=RequestContext(request))
        return response

    return HttpResponseForbidden()


@csrf_exempt
def remove_writein_from_cart(request, item_id):
    """Removes the writein item with item_id from the cart associated with the
    session."""
    if request.method == 'POST':
        cart = get_session_cart(request.session)
        cart.remove_writein_item(item_id)

        response = render_to_response(
            'cart.html', {'cart': cart},
            context_instance=RequestContext(request))
        return response

    return HttpResponseForbidden()


@csrf_exempt
def remove_virtualshop_item_from_cart(request, item_id):
    """Removes the virtual shop item writh item_id from the cart associated
    with the session."""
    if request.method == "POST":
        cart = get_session_cart(request.session)
        cart.remove_virtualshop_item(item_id)

        response = render_to_response(
            'cart.html', {'cart': cart},
            context_instance=RequestContext(request))
        return response

    return HttpResponseForbidden()


@csrf_exempt
def empty_cart(request):
    """Emptys the cart object associated with the session."""
    if request.method == "POST":
        cart = get_session_cart(request.session)
        cart.empty()
        return render_to_response(
            'cart.html', {'cart': cart},
            context_instance=RequestContext(request))

    return HttpResponseForbidden()


@csrf_exempt
def review(request):
    """Review the current cart and collect user info."""

    # Get the cart from the session (if one exists)
    cart = get_session_cart(request.session)

    return render_to_response(
        'review.html', {'cart': cart,
                        'member_name': cart.cart_username,
                        'member_email': cart.cart_useremail,
                        'member_phone': cart.cart_userphone,
                        'order_comments': cart.cart_comment},
        context_instance=RequestContext(request))


@csrf_exempt
def submit(request):
    """Validates and emails the cart and member details to FNs team."""

    cart = get_session_cart(request.session)

    member_name = request.POST.get('member_name', '')
    member_phone = request.POST.get('member_phone', '')
    member_email = request.POST.get('member_email', '')
    order_comments = request.POST.get('order_comments', '')

    # member_email shouldn't have trailing whitespace
    member_email = member_email.strip()

    # Validate the form and cart.
    isValid = True
    if cart.num_items == 0:
        isValid = False
        request.notifications.create("There are no items your shopping list!",
                                     'error')
    if len(member_name) == 0:
        isValid = False
        request.notifications.create("Please enter your name", 'error')
    if len(member_phone) == 0:
        isValid = False
        request.notifications.create(
            "Please provide a phone number in case we need to contact you",
            'error')
    if len(member_email) == 0 or not isAddressValid(member_email):
        isValid = False
        request.notifications.create(
            "Please check that your email address is valid", 'error')

    # If it's valid, make the rtf, attach and send to the email, clear the
    # cart and return success page.
    if isValid:
        # store the result of createOrderForm (a StringIO object) in a buffer.
        buffer = createOrderForm(cart, request.POST)

        email_to = []
        email_to.extend([ORDER_FORM_REPLY_TO_EMAIL])
        email_to.append(member_email)

        email_message = 'Order attached. \n\n'
        if order_comments:
            email_message += 'The order has the following comments:\n'
            email_message += '#####################\n\n'
            email_message += order_comments
            email_message += '\n\n'

        slug_name = slugify(member_name)

        success = False
        # Try making and sending the email.
        try:
            mail = EmailMessage(
                '[FruityNuttersOrder] {0}'.format(member_name),
                email_message, ORDER_FORM_SEND_EMAIL, email_to,
                headers={'Reply-To': ORDER_FORM_REPLY_TO_EMAIL})
            mail.attach('{0}_order_form.rtf'.format(slug_name),
                        buffer.getvalue(),
                        'application/rtf')
            mail.send()
        except SMTPException as e:
            request.notifications.create(
                "There was a problem submitting your order :( . "
                "Please email {0} to let us know what is says here: "
                "{1}".format(ORDER_FORM_REPLY_TO_EMAIL, str(e)), 'error')
        else:
            # Don't need the cart anymore; empty it.
            cart.empty()
            cart.delete()
            cart.save()

            success = True
            request.notifications.create(
                "Your order has been submitted! Ta very much!", 'success')
        finally:
            buffer.close()

        return render_to_response('review.html', {'cart': cart,
                                                  'submit_success': success},
                                  context_instance=RequestContext(request))

    # Else if the form isn't valid...
    else:
        return render_to_response('review.html',
                                  {'cart': cart,
                                   'member_name': member_name,
                                   'member_email': member_email,
                                   'member_phone': member_phone,
                                   'order_comments': order_comments},
                                  context_instance=RequestContext(request))


@csrf_exempt
def save_cart_details(request):
    if request.method == 'POST':
        cart = get_session_cart(request.session)

        member_name = request.POST.get('member_name', '')
        member_phone = request.POST.get('member_phone', '')
        member_email = request.POST.get('member_email', '')
        order_comments = request.POST.get('order_comments', '')

        cart.cart_comment = order_comments
        cart.cart_username = member_name
        cart.cart_useremail = member_email
        cart.cart_userphone = member_phone
        cart.save()

        return HttpResponse("Comment saved successfully!",
                            content_type="text/plain")

    return HttpResponseForbidden()
