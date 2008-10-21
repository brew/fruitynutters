# -*- coding: utf-8 -*-

from rtfng.Elements import StyleSheet, Document
from rtfng.Styles import TextStyle, ParagraphStyle
from rtfng.PropertySets import TextPropertySet, ParagraphPropertySet, TabPropertySet, BorderPropertySet, FramePropertySet
from rtfng.document.section import Section
from rtfng.document.paragraph import Paragraph, Table, Cell

def createOrderForm(cart, member_details):
    """Creates and returns an order form pdf."""

    member_name = member_details.get('member_name')
    member_email = member_details.get('member_email')
    member_phone = member_details.get('member_phone')

    ss = makeReportStylesheet()
    doc = Document(ss)
    section = Section()
    doc.Sections.append( section )

    footer_text = "Order for: " + member_name + ", phone: " + member_phone
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
        