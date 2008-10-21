# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden, HttpResponse
from django.template import RequestContext

from fruitynutters.catalogue.models import Item
from fruitynutters.cart.models import Cart, CartItem
from fruitynutters.util import get_session_cart

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
    # response = render_to_response('order_form.rtf', {'cart':cart}, context_instance=RequestContext(request), mimetype = 'application/rtf')
    response['Content-Disposition'] = 'attachment;filename=order_form.rtf'

    document_renderer = Renderer()
    document_renderer.Write(createOrderForm(cart, request.POST), response)

    return response


from rtfng.Renderer import Renderer
from rtfng.Elements import StyleSheet, Document
from rtfng.Styles import TextStyle, ParagraphStyle
from rtfng.PropertySets import TextPropertySet, ParagraphPropertySet, TabPropertySet, BorderPropertySet, FramePropertySet
from rtfng.document.section import Section
from rtfng.document.paragraph import Paragraph, Table, Cell
    
def createOrderForm(cart, member_details):
    
    member_name = member_details.get('member_name')
    member_email = member_details.get('member_email')
    member_phone = member_details.get('member_phone')
    
    """Creates and returns an order form pdf."""
    ss = makeReportStylesheet()
    doc = Document(ss)
    section = Section()
    doc.Sections.append( section )
    
    footer_text = "Order for: " + member_name
    section.Footer.append(str(footer_text))

    table = Table(  TabPropertySet.DEFAULT_WIDTH,
                    TabPropertySet.DEFAULT_WIDTH * 8,
                    TabPropertySet.DEFAULT_WIDTH * 2,
                    TabPropertySet.DEFAULT_WIDTH * 2 )

    thin_edge  = BorderPropertySet( width=10, style=BorderPropertySet.SINGLE )
    thin_frame  = FramePropertySet( thin_edge,  thin_edge,  thin_edge,  thin_edge )

    # header
    header_props = ParagraphPropertySet(alignment=3)

    c1_para = Paragraph(ss.ParagraphStyles.Heading2, header_props)
    c1_para.append('O')
    c1 = Cell(c1_para, thin_frame)
    
    c2_para = Paragraph(header_props)
    c2_para.append('Product ordered')
    c2 = Cell(c2_para, thin_frame )

    c3_para = Paragraph(header_props)
    c3_para.append('Amount')
    c3 = Cell(c3_para, thin_frame )
    
    c4_para = Paragraph(header_props)
    c4_para.append('Cost')
    c4 = Cell(c4_para, thin_frame )
    table.AddRow(c1, c2, c3, c4)

    # list
    for cart_item in cart.cartitem_set.all():
        organic = ""
        if cart_item.product.organic:
            organic = "o"
        
        centre_props = ParagraphPropertySet(alignment=3)    
        
        c1_para = Paragraph(ss.ParagraphStyles.Normal, centre_props)
        c1_para.append(organic)
        c1 = Cell(c1_para, thin_frame)

        measure_per_unit = "%g" % cart_item.product.measure_per_unit
        
        c2_para = Paragraph()
        c2_para.append(unicode(cart_item.product.name) + " (" + unicode(cart_item.product.unit_number) + " x " + str(measure_per_unit) + unicode(cart_item.product.measure_type) + ")")
        c2 = Cell(c2_para, thin_frame)
        
        c3_para = Paragraph(centre_props)
        c3_para.append(unicode(cart_item.quantity))
        c3 = Cell(c3_para, thin_frame)
        
        cost_props = ParagraphPropertySet(alignment=2)
        
        c4_para = Paragraph(cost_props)
        c4_para.append(unicode(cart_item.line_total))
        c4 = Cell(c4_para, thin_frame)
        table.AddRow(c1, c2, c3, c4)


    c1_para = Paragraph(ss.ParagraphStyles.Heading2, ParagraphPropertySet(alignment=2))
    c1_para.append('Total cost')
    c1 = Cell(c1_para, thin_frame, span=3)
    
    c2_para = Paragraph(ParagraphPropertySet(alignment=2))
    c2_para.append(u"£"+str(cart.total))
    c2 = Cell(c2_para,thin_frame)
    table.AddRow(c1,c2)

    section.append( table )

    return doc
    
def makeReportStylesheet():
    result = StyleSheet()

    NormalText = TextStyle( TextPropertySet( result.Fonts.Arial, 20 ) )

    ps = ParagraphStyle( 'Normal',
                         NormalText.Copy(),
                         ParagraphPropertySet( space_before = 60,
                                               space_after  = 60 ) )
    result.ParagraphStyles.append( ps )

    ps = ParagraphStyle( 'Normal Short',
                         NormalText.Copy() )
    result.ParagraphStyles.append( ps )

    NormalText.textProps.size = 32
    ps = ParagraphStyle( 'Heading 1',
                         NormalText.Copy(),
                         ParagraphPropertySet( space_before = 240,
                                               space_after  = 60 ) )
    result.ParagraphStyles.append( ps )

    NormalText.textProps.size = 24
    NormalText.textProps.bold = True
    ps = ParagraphStyle( 'Heading 2',
                         NormalText.Copy(),
                         ParagraphPropertySet( space_before = 240,
                                               space_after  = 60 ) )
    result.ParagraphStyles.append( ps )

    return result
