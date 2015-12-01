import os
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Frame
from reportlab.lib.styles import getSampleStyleSheet


# Create your views here.
def generatePDF(request):
    order = {'filename': 'test_pdf.pdf',
             'bodyType': 'SUV', 'engine': '1.6LV6', 'color': 'Red',
             'transmission': 'Auto', 'stock': '103338', 'mileage': '14000 km',
             'vehicle_name': '2016 Honda Pilot EX-L Navi', 'price': '$47,185',
             'link': 'https://www.youtube.com/watch?v=tkwZ1jG3XgA',

             'customer_name': 'First Last', 'email': 'email@gmail.com',
             'phone': '3030000000', 'postalcode': '123 409',

             'trade_year': '2001', 'trade_make': 'Honda', 'trade_model': 'Civic',
             'trade_trim': 'LE', 'trade_vin': '1234'
             }
    # response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % order['filename']
    pdf = GeneratePDF(order)
    return HttpResponse("ok")


class GeneratePDF:
    def __init__(self, order_data):
        # self.buffer = BytesIO()
        self.order_data = order_data
        self.doc = SimpleDocTemplate(os.path.join('uploads/pdfs', order_data['filename']), pagesize=A4, rightMargin=30,
                                     leftMargin=30,
                                     topMargin=5,
                                     bottomMargin=18)
        self.elements = []
        self.styles = getSampleStyleSheet()

        self.header()
        self.customer_table()
        self.new_vehicle_table()
        self.trade_table()
        self.save_pdf()

    def save_pdf(self):
        self.doc.build(self.elements)
        # pdf = self.buffer.getvalue()
        # self.buffer.close()
        # return pdf

    def header(self):
        img = Image("http://design.ubuntu.com/wp-content/uploads/ubuntu-logo32.png")
        img.drawHeight = 1.25*inch*img.drawHeight / img.drawWidth
        img.drawWidth = 1.25*inch
        title = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PDF Sample", self.styles["Heading2"])

        img_title_data = [
            [img, title]
        ]

        img_title_table_style = TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                          ('ALIGN', (-1, -1), (-1, -1), 'CENTER'),
                                          ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
                                          ])

        img_title_table = Table(img_title_data)
        img_title_table.setStyle(img_title_table_style)

        self.elements.append(img_title_table)
        self.elements.append(Paragraph("Generated on %s" % timezone.now(), self.styles["Normal"]))
        self.elements.append(Paragraph("<b>&nbsp;</b>", self.styles["Heading1"]))

    def new_vehicle_table(self):
        name = Paragraph('''<b><font color=red>%s</font></b>''' % self.order_data['vehicle_name'],
                         self.styles["Heading2"])
        price = Paragraph('''<font color=green>Price: %s</font>''' % self.order_data['price'], self.styles["Heading2"])

        name_price_data = [
            [name, price]
        ]
        name_price_table = Table(name_price_data)
        name_price_table._argW[0] = 5.8 * inch

        vehicle_data = [
            ["<b>Body Style:</b>", self.order_data['bodyType'], "<b>Transmission:</b>",
             self.order_data['transmission']],
            ["<b>Engine:</b>", self.order_data['engine'], "<b>Stock #:</b>", self.order_data['stock']],
            ["<b>Exterior Colour:</b>", self.order_data['color'], "<b>Mileage:</b>", self.order_data['mileage']],
        ]

        vehicle_table_style = TableStyle([('TEXTCOLOR', (0, 0), (1, 2), colors.blue),
                                          ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                                          ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                          ('BACKGROUND', (0, 0), (3, 0), HexColor('#F2F2F2')),
                                          ('BACKGROUND', (0, 1), (3, 1), HexColor('#fbfbfb')),
                                          ('BACKGROUND', (0, 2), (3, 2), HexColor('#F2F2F2')),
                                          ])
        style = self.styles["BodyText"]
        style.wordWrap = 'CJK'
        new_vehicle_data = [[Paragraph(cell, style) for cell in row] for row in vehicle_data]
        vehicle_table = Table(new_vehicle_data)
        vehicle_table.setStyle(vehicle_table_style)

        self.elements.append(Paragraph("Vehicle Information:", self.styles["Heading1"]))
        self.elements.append(name_price_table)
        self.elements.append(vehicle_table)
        self.elements.append(Paragraph("<u><a href='%s' color='blue'>Open Vehicle in Browser</a></u>" % self.order_data['link'], self.styles["Normal"]))

        self.elements.append(Paragraph("<b>&nbsp;</b>", self.styles["Heading1"]))

    def customer_table(self):
        self.elements.append(Paragraph("Customer Information:", self.styles["Heading1"]))

        name = Paragraph(
            '''<b><font color=red>%s</font></b>''' % self.order_data['customer_name'],
            self.styles["Heading2"])
        self.elements.append(name)

        other_customer_data = [
            ["<b>Email:</b>", self.order_data['email'], "<b>Phone:</b>", self.order_data['phone']],
            ["<b>Postal Code:</b>", self.order_data['postalcode']],
        ]

        customer_table_style = TableStyle([('TEXTCOLOR', (0, 0), (1, 1), colors.blue),
                                           ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                           ('BACKGROUND', (0, 0), (3, 0), HexColor('#F2F2F2')),
                                           ('BACKGROUND', (0, 1), (3, 1), HexColor('#fbfbfb')),
                                           ])
        style = self.styles["BodyText"]
        style.wordWrap = 'CJK'
        new_customer_data = [[Paragraph(cell, style) for cell in row] for row in other_customer_data]
        customer_table = Table(new_customer_data)
        customer_table.setStyle(customer_table_style)

        self.elements.append(customer_table)
        self.elements.append(Paragraph("<b>&nbsp;</b>", self.styles["Heading1"]))

    def trade_table(self):
        self.elements.append(Paragraph("Trade Information:", self.styles["Heading1"]))

        vin = Paragraph(
            '''<b><font color=red>%s</font></b>''' % self.order_data['trade_vin'],
            self.styles["Heading2"])
        self.elements.append(vin)

        trade_data = [
            ["<b>Year:</b>", self.order_data['trade_year'], "<b>Make:</b>", self.order_data['trade_make']],
            ["<b>Model:</b>", self.order_data['trade_model'], "<b>Trim:</b>", self.order_data['trade_trim']],
        ]

        trade_table_style = TableStyle([('TEXTCOLOR', (0, 0), (1, 1), colors.blue),
                                           ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                           ('BACKGROUND', (0, 0), (3, 0), HexColor('#F2F2F2')),
                                           ('BACKGROUND', (0, 1), (3, 1), HexColor('#fbfbfb')),
                                           ])
        style = self.styles["BodyText"]
        style.wordWrap = 'CJK'
        new_trade_data = [[Paragraph(cell, style) for cell in row] for row in trade_data]
        trade_table = Table(new_trade_data)
        trade_table.setStyle(trade_table_style)

        self.elements.append(trade_table)
        self.elements.append(Paragraph("<b>&nbsp;</b>", self.styles["Heading1"]))