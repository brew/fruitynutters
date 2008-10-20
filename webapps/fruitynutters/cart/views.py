from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden, HttpResponse
from django.template import RequestContext

from fruitynutters.catalogue.models import Item
from fruitynutters.cart.models import Cart, CartItem
from fruitynutters.util import get_session_cart

from PyRTF import *

def add_to_cart(request, item_id, quantity=1):
    """Adds the item with item_id to the cart associated with the session."""
    if request.method == 'POST':        
        
        quantity = int(quantity)
        cart = get_session_cart(request.session)

        bundle = None
        # If there are items in the post request, then there are bundle items to deal with.
        # Use a list comp to create a new list containing the actual item and quantity. Only if the quantity is more than 0.
        if request.POST.items():
            bundle = [(Item.objects.get(id__exact=bi[0]), int(bi[1])) for bi in request.POST.items() if bi[1] != "" and int(bi[1]) > 0]
            request.notifications.create(Cart.CART_BUNDLE_ADDED_NOTICE, 'cart_information')
        
        item_to_add = Item.objects.get(id__exact=item_id)
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
    
    response = HttpResponse(mimetype = 'application/rtf')
    response['Content-Disposition'] = 'attachment;filename=order_form.rtf'

    document_renderer = Renderer()
    document_renderer.Write(createOrderForm(cart, request.POST), response)
    
    return response
    
def createOrderForm(cart, member_details):
    """Creates and returns an order form pdf."""
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section()
    doc.Sections.append( section )

    # p = Paragraph( ss.ParagraphStyles.Heading1 )
    # p.append( 'Example 3' )
    # section.append( p )

    # changes what is now the default style of Heading1 back to Normal
    # p = Paragraph( ss.ParagraphStyles.Normal )
    # p.append( 'Example 3 demonstrates tables, tables represent one of the '
    #             'harder things to control in RTF as they offer alot of '
    #             'flexibility in formatting and layout.' )
    # section.append( p )

    # section.append( 'Table columns are specified in widths, the following example '
    #                 'consists of a table with 3 columns, the first column is '
    #                 '7 tab widths wide, the next two are 3 tab widths wide. '
    #                 'The widths chosen are arbitrary, they do not have to be '
    #                 'multiples of tab widths.' )

    table = Table(  TabPS.DEFAULT_WIDTH,
                    TabPS.DEFAULT_WIDTH * 7,
                    TabPS.DEFAULT_WIDTH * 2,
                    TabPS.DEFAULT_WIDTH * 2 )

    thin_edge  = BorderPS( width=10, style=BorderPS.SINGLE )
    thin_frame  = FramePS( thin_edge,  thin_edge,  thin_edge,  thin_edge )

    c1 = Cell( Paragraph( ss.ParagraphStyles.Heading2, 'O'), thin_frame)
    c2 = Cell( Paragraph( ss.ParagraphStyles.Heading2, 'Product ordered'), thin_frame )
    c2.SetAlignment(2)
    c3 = Cell( Paragraph( ss.ParagraphStyles.Heading2, 'Amount'), thin_frame )
    c4 = Cell( Paragraph( ss.ParagraphStyles.Heading2, 'Cost'), thin_frame )
    table.AddRow(c1, c2, c3, c4)


    for cart_item in cart.cartitem_set.all():
        organic = ""
        if cart_item.product.organic:
            organic = "o"
        c1 = Cell( Paragraph(ss.ParagraphStyles.Normal, str(organic)), thin_frame)
        c2 = Cell( Paragraph(ss.ParagraphStyles.Normal, str(cart_item.product.name)), thin_frame)
        c3 = Cell( Paragraph(ss.ParagraphStyles.Normal, str(cart_item.quantity) + " x " + str(cart_item.product.measure_per_unit) + str(cart_item.product.measure_type)), thin_frame)
        c4 = Cell( Paragraph(ss.ParagraphStyles.Normal, str(cart_item.line_total)), thin_frame)
        table.AddRow(c1, c2, c3, c4)

    # c1 = Cell( Paragraph( ss.ParagraphStyles.Heading2, 'Heading2 Style'   ) )
    # c2 = Cell( Paragraph( ss.ParagraphStyles.Normal, 'Back to Normal Style'   ) )
    # c3 = Cell( Paragraph( 'More Normal Style' ) )
    # table.AddRow( c1, c2, c3 )

    # c1 = Cell( Paragraph( ss.ParagraphStyles.Heading2, 'Heading2 Style'   ) )
    # c2 = Cell( Paragraph( ss.ParagraphStyles.Normal, 'Back to Normal Style'   ) )
    # c3 = Cell( Paragraph( 'More Normal Style' ) )
    # table.AddRow( c1, c2, c3 )

    section.append( table )
    # section.append( 'Different frames can also be specified for each cell in the table '
    #                  'and each frame can have a different width and style for each border.' )
    # 
    #  thin_edge  = BorderPS( width=20, style=BorderPS.SINGLE )
    #  thick_edge = BorderPS( width=80, style=BorderPS.SINGLE )
    # 
    #  thin_frame  = FramePS( thin_edge,  thin_edge,  thin_edge,  thin_edge )
    #  thick_frame = FramePS( thick_edge, thick_edge, thick_edge, thick_edge )
    #  mixed_frame = FramePS( thin_edge,  thick_edge, thin_edge,  thick_edge )
    # 
    #  table = Table( TabPS.DEFAULT_WIDTH * 3, TabPS.DEFAULT_WIDTH * 3, TabPS.DEFAULT_WIDTH * 3 )
    #  c1 = Cell( Paragraph( 'R1C1' ), thin_frame )
    #  c2 = Cell( Paragraph( 'R1C2' ) )
    #  c3 = Cell( Paragraph( 'R1C3' ), thick_frame )
    #  table.AddRow( c1, c2, c3 )
    # 
    #  c1 = Cell( Paragraph( 'R2C1' ) )
    #  c2 = Cell( Paragraph( 'R2C2' ) )
    #  c3 = Cell( Paragraph( 'R2C3' ) )
    #  table.AddRow( c1, c2, c3 )
    # 
    #  c1 = Cell( Paragraph( 'R3C1' ), mixed_frame )
    #  c2 = Cell( Paragraph( 'R3C2' ) )
    #  c3 = Cell( Paragraph( 'R3C3' ), mixed_frame )
    #  table.AddRow( c1, c2, c3 )
    # 
    #  section.append( table )
    # 
    #  section.append( 'In fact frames can be applied to paragraphs too, not just cells.' )
    # 
    #  p = Paragraph( ss.ParagraphStyles.Normal, thin_frame )
    #  p.append( 'This whole paragraph is in a frame.' )
    #  section.append( p )
    return doc
    
    
    
    
    
