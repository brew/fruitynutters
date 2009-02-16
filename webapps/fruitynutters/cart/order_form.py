# -*- coding: utf-8 -*-

from rtfng.Elements import StyleSheet, Document
from rtfng.Styles import TextStyle, ParagraphStyle
from rtfng.PropertySets import TextPropertySet, ParagraphPropertySet, TabPropertySet, BorderPropertySet, FramePropertySet, MarginsPropertySet, Paper
from rtfng.document.section import Section
from rtfng.document.paragraph import Paragraph, Table, Cell
from rtfng.Constants import Languages
from rtfng.Renderer import Renderer

from cStringIO import StringIO

def createOrderForm(cart, member_details):
    """Creates and returns an order form pdf."""

    member_name = unicode(member_details.get('member_name'))
    member_email = unicode(member_details.get('member_email'))
    member_phone = unicode(member_details.get('member_phone'))
    order_comments = unicode(member_details.get('order_comments'))

    ss = makeReportStylesheet()
    doc = Document(ss, default_language=Languages.EnglishUK)
    paper = Paper('A4', 9, 'A4 297 x 210 mm', 16838, 11907)
    section = Section(margins=MarginsPropertySet( top=100, left=400, bottom=100, right=400 ), paper=paper, landscape=True, headery=0, footery=300)
    doc.Sections.append( section )

    footer_text = member_name + " " + member_phone
    footer_p = Paragraph(ss.ParagraphStyles.Heading1)
    footer_p.append(unicode(footer_text)) 
    section.Footer.append(footer_p)

    thin_edge  = BorderPropertySet( width=10, style=BorderPropertySet.SINGLE )
    thin_frame  = FramePropertySet( thin_edge,  thin_edge,  thin_edge,  thin_edge )

    # based on twirps or 567/cm.
    table = Table(  3118,
                    567,
                    709 )

    # header
    header_props = ParagraphPropertySet(alignment=3)

    c2_para = Paragraph(ss.ParagraphStyles.Normal, header_props)
    c2_para.append(u'Product')
    c2 = Cell(c2_para, thin_frame )

    c3_para = Paragraph(ss.ParagraphStyles.Normal, header_props)
    c3_para.append(u'No.')
    c3 = Cell(c3_para, thin_frame )

    c4_para = Paragraph(ss.ParagraphStyles.Normal, header_props)
    c4_para.append(u'Cost')
    c4 = Cell(c4_para, thin_frame )
    table.AddRow(c2, c3, c4)

    # list
    for cart_item in cart.cartitem_set.all().order_by('product__picking_order', 'product__aisle', 'product__sort_name'):
        centre_props = ParagraphPropertySet(alignment=3)    

        c2_para = Paragraph(ss.ParagraphStyles.Normal)
        c2_para.append(unicode(cart_item.product.order_name))

        if cart_item.product.bundle:
            c2_para.append(u": ")
            for bundle_item in cart_item.cart_bundle.cartitem_set.all():
                c2_para.append(unicode(bundle_item.product.order_name))
                c2_para.append(u" x " + unicode(bundle_item.quantity) + u", ")
        c2 = Cell(c2_para, thin_frame)

        c3_para = Paragraph(centre_props)
        c3_para.append(unicode(cart_item.quantity))
        c3 = Cell(c3_para, thin_frame)

        cost_props = ParagraphPropertySet(alignment=2)

        c4_para = Paragraph(cost_props)
        c4_para.append(unicode(cart_item.line_total))
        c4 = Cell(c4_para, thin_frame)
        table.AddRow(c2, c3, c4)

    # table footer
    c1_para = Paragraph(ss.ParagraphStyles.Heading2Short, ParagraphPropertySet(alignment=2))
    c1_para.append(u'Total cost')
    c1 = Cell(c1_para, thin_frame, span=2)

    c2_para = Paragraph(ParagraphPropertySet(alignment=2))
    c2_para.append(unicode(cart.total))
    c2 = Cell(c2_para,thin_frame)
    table.AddRow(c1,c2)
    
    # write ins
    for writein_item in cart.cartwriteinitem_set.all():
        centre_props = ParagraphPropertySet(alignment=3)    

        c2_para = Paragraph(ss.ParagraphStyles.Normal)
        c2_para.append(unicode(writein_item.name) + u" -- " + unicode(writein_item.code))
        c2 = Cell(c2_para, thin_frame)

        c3_para = Paragraph(centre_props)
        # c3_para.append(unicode(cart_item.quantity))
        c3 = Cell(c3_para, thin_frame)

        cost_props = ParagraphPropertySet(alignment=2)

        c4_para = Paragraph(cost_props)
        # c4_para.append(unicode(cart_item.line_total))
        c4 = Cell(c4_para, thin_frame)
        table.AddRow(c2, c3, c4)
        
    # virtual shop items.
    for virtualshop_item in cart.cartvirtualshopitem_set.all():
        centre_props = ParagraphPropertySet(alignment=3)
    
        c2_para = Paragraph(ss.ParagraphStyles.Normal)
        c2_para.append(unicode(virtualshop_item.name) + u" -- VS")
        c2 = Cell(c2_para, thin_frame)

        c3_para = Paragraph(centre_props)
        c3_para.append(unicode(virtualshop_item.quantity))
        c3 = Cell(c3_para, thin_frame)

        cost_props = ParagraphPropertySet(alignment=2)

        c4_para = Paragraph(cost_props)
        # c4_para.append(unicode(cart_item.line_total))
        c4 = Cell(c4_para, thin_frame)
        table.AddRow(c2, c3, c4)
    

    section.append( table )
    
    section.append(Paragraph())

    rtf_doc = StringIO()

    document_renderer = Renderer()
    document_renderer.Write(doc, rtf_doc)    

    return rtf_doc

def makeReportStylesheet():
    result = StyleSheet()

    NormalText = TextStyle( TextPropertySet( result.Fonts.Arial, 16 ) )

    ps = ParagraphStyle( 'Normal',
                         NormalText.Copy(),
                         ParagraphPropertySet( space_before = 30,
                                               space_after  = 30 ) )
    result.ParagraphStyles.append( ps )

    ps = ParagraphStyle( 'Normal Short',
                         NormalText.Copy() )
    result.ParagraphStyles.append( ps )

    NormalText.textProps.size = 24
    ps = ParagraphStyle( 'Heading 1',
                         NormalText.Copy(),
                         ParagraphPropertySet( space_before = 30,
                                               space_after  = 60 ) )
    result.ParagraphStyles.append( ps )

    NormalText.textProps.size = 12
    NormalText.textProps.bold = True
    ps = ParagraphStyle( 'Heading 2',
                         NormalText.Copy(),
                         ParagraphPropertySet( space_before = 39,
                                               space_after  = 60 ) )
    result.ParagraphStyles.append( ps )
    
    NormalText.textProps.size = 16
    NormalText.textProps.bold = True
    ps = ParagraphStyle( 'Heading 2 Short',
                         NormalText.Copy() )

    result.ParagraphStyles.append( ps )
    

    return result
        