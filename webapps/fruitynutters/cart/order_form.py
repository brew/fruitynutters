# -*- coding: utf-8 -*-

from rtfng.Elements import StyleSheet, Document
from rtfng.Styles import TextStyle, ParagraphStyle
from rtfng.PropertySets import TextPropertySet, ParagraphPropertySet, TabPropertySet, BorderPropertySet, FramePropertySet, MarginsPropertySet
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
    section = Section(margins=MarginsPropertySet( top=600, left=600, bottom=600, right=600 ))
    doc.Sections.append( section )

    header_text = Paragraph(ss.ParagraphStyles.Heading2Short, ParagraphPropertySet(alignment=3))
    header_text.append(u"Fruity Nutters - Order form")
    section.Header.append(header_text)

    footer_text = member_name + u" -  Phone: " + member_phone
    
    if len(member_email) > 0:
        footer_text += u" - Email: " + member_email
    section.Footer.append(unicode(footer_text))

    thin_edge  = BorderPropertySet( width=10, style=BorderPropertySet.SINGLE )
    thin_frame  = FramePropertySet( thin_edge,  thin_edge,  thin_edge,  thin_edge )

    table = Table(  TabPropertySet.DEFAULT_WIDTH,
                    TabPropertySet.DEFAULT_WIDTH * 9,
                    TabPropertySet.DEFAULT_WIDTH * 2,
                    TabPropertySet.DEFAULT_WIDTH * 2 )

    # header
    header_props = ParagraphPropertySet(alignment=3)

    c1_para = Paragraph(ss.ParagraphStyles.Heading2Short, header_props)
    c1_para.append('O')
    c1 = Cell(c1_para, thin_frame)

    c2_para = Paragraph(header_props)
    c2_para.append(u'Product ordered')
    c2 = Cell(c2_para, thin_frame )

    c3_para = Paragraph(header_props)
    c3_para.append(u'Amount')
    c3 = Cell(c3_para, thin_frame )

    c4_para = Paragraph(header_props)
    c4_para.append(u'Cost')
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
        c2_para.append(unicode(cart_item.product.name))
        brand = cart_item.product.brand
        if brand:
            c2_para.append(" - " + unicode(brand))
        c2_para.append(" (" + unicode(cart_item.product.unit_number) + " x " + unicode(measure_per_unit) + unicode(cart_item.product.measure_type) + ")")
        if cart_item.product.bundle:
            c2_para.append(u"\n")
            for bundle_item in cart_item.cart_bundle.cartitem_set.all():
                c2_para.append(unicode(bundle_item.product.name))
                c2_para.append(u" x " + unicode(bundle_item.quantity) + u", ")
        c2 = Cell(c2_para, thin_frame)

        c3_para = Paragraph(centre_props)
        c3_para.append(unicode(cart_item.quantity))
        c3 = Cell(c3_para, thin_frame)

        cost_props = ParagraphPropertySet(alignment=2)

        c4_para = Paragraph(cost_props)
        c4_para.append(unicode(cart_item.line_total))
        c4 = Cell(c4_para, thin_frame)
        table.AddRow(c1, c2, c3, c4)

    # table footer
    c1_para = Paragraph(ss.ParagraphStyles.Heading2Short, ParagraphPropertySet(alignment=2))
    c1_para.append(u'Total cost')
    c1 = Cell(c1_para, thin_frame, span=3)

    c2_para = Paragraph(ParagraphPropertySet(alignment=2))
    c2_para.append(u"£"+unicode(cart.total))
    c2 = Cell(c2_para,thin_frame)
    table.AddRow(c1,c2)

    section.append( table )
    
    section.append(Paragraph())

    # Comments / Wishlist
    comments_header = Paragraph(ss.ParagraphStyles.Heading2Short)
    comments_header.append(u'Comments / Wishlist')
    section.append(comments_header)
    
    table = Table(10000)
    
    comments_para = Paragraph(ss.ParagraphStyles.Normal)
    comments_para.append( order_comments )
    c1 = Cell(comments_para, thin_frame)
    table.AddRow(c1)
    
    section.append(table)
    
    section.append(Paragraph())    
    
    # admin table
    table = Table(  TabPropertySet.DEFAULT_WIDTH * 7,
                    TabPropertySet.DEFAULT_WIDTH * 7)
                    
    c1_para = Paragraph(ss.ParagraphStyles.AdminPara)
    c1_para.append(u'Extras')
    c1 = Cell(c1_para, thin_frame)

    c2_para = Paragraph()
    c2_para.append(u'Refunds')
    c2 = Cell(c2_para, thin_frame )    
    table.AddRow(c1, c2)
    
    c1_para = Paragraph(ss.ParagraphStyles.AdminPara)
    c1 = Cell(c1_para, thin_frame)

    c2_para = Paragraph()
    c2_para.append(u'Paid')
    c2 = Cell(c2_para, thin_frame )    
    table.AddRow(c1, c2)
    
    section.append(table)

    rtf_doc = StringIO()

    document_renderer = Renderer()
    document_renderer.Write(doc, rtf_doc)    

    return rtf_doc

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
    
    NormalText.textProps.size = 24
    NormalText.textProps.bold = True
    ps = ParagraphStyle( 'Heading 2 Short',
                         NormalText.Copy() )

    result.ParagraphStyles.append( ps )
    
    result.ParagraphStyles.append(ParagraphStyle('Admin Para',
                                NormalText.Copy(),
                                ParagraphPropertySet(space_after = 2000)) )
                                
    result.ParagraphStyles.append(ParagraphStyle('Comments',
                                NormalText.Copy(),
                                ParagraphPropertySet(space_after = 200, space_before=200, left_indent=200, right_indent=200)) )

    return result
        