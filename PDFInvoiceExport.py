import pygame, sys
from weasyprint import HTML, CSS
from gui.Controls import CreateTitle, Background, Button
import time
import json

green = (156, 219, 151)
green_bright = (0,150,0)
emptyBackground = pygame.image.load("assets/empty_background.png")

class Engine():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.event = None

    def main_loop(self, objects, items):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for object in objects:
                object.update(event, "")
                self.handler = object.update(event, "")

                if self.handler == "downloadInvoice":
                    GenerateInvoice().invoice(items)

            pygame.display.update()
            self.clock.tick(self.fps)

class InvoiceView():
    def __init__(self, items=None):
        self.display = pygame.display.set_mode((600,510))
        pygame.display.set_caption('Generate Invoice')
        self.items = items
        self.objects = [
            Background(self.display, emptyBackground), # Setting the background
            CreateTitle(self.display, "Do you want to download your invoice?", 24, 40),
            Button(self.display, "DOWNLOAD INVOICE", 190, 280, 223, 48, green, green_bright, "downloadInvoice")
        ]
        # Adding all of the components in an array

        Engine().main_loop(self.objects, self.items)
        # running the main loop and giving the array as parameter

    def get_items(self):
        return self.items

class GenerateInvoice():
    def __init__(self):
        pass

    def bubbleSort(self, listForSort):
        for passnum in range(len(listForSort)-1,0,-1):
            for i in range(passnum):
                if listForSort[i]['productPrice']>listForSort[i+1]['productPrice']:
                    temp = listForSort[i]
                    listForSort[i] = listForSort[i+1]
                    listForSort[i+1] = temp

    def insertionSort(self, listForSort):
        for index in range(1,len(listForSort)):

            currentvalue = listForSort[index]
            position = index

            while position > 0 and listForSort[position-1]['productPrice'] > currentvalue['productPrice']:
                listForSort[position]=listForSort[position-1]
                position = position-1

            listForSort[position]=currentvalue

    def invoice(self, items):
        today = time.strftime("%d/%m/%Y")
        invoiceItems = ""
        totalAmount = 0
        self.bubbleSort(items)

        for selectedProduct in items:
            totalAmount = totalAmount + selectedProduct['productPrice']
            invoiceItems = invoiceItems + "<tr><td>" + selectedProduct['productTitle'] + "</td><td>" + str(selectedProduct['productWeight']) + " kg</td><td>£" + str(selectedProduct['productPrice']) + "</td></tr>"

        firstPart = '''
        <html>
            <body style="width: 100%">
                <div class="header">
                    <img style="width: 200px" src="http://donchev.net/blog/ads_drone.png" alt="" />
                </div>
                <div style="padding-top: 60px; float:left; width: 100%;">
                    <div style="width: 60%;float:left">
                    <h2>billed to</h2>
                    <p>Nikola Donchev</p>
                    <p>Coventry, UK</p>
                    <p>CV1 5AX</p>
                </div>
                <div style="width: 40%;float:left">
                    <p>Invoice number: 43432</p>
                    <p>Date: ''' + today + '''</p>
                    <p style="background-color: #cacaca">Total amount: £''' + str(totalAmount) + '''</p>
                </div>
                <div style="clear: both"></div>
                <hr>
                <table style="width:100%; padding-top: 20px;">
                    <tr style="border-bottom: 5px solid #6b6b6b">
                        <th>Product name</th>
                        <th>Weight</th>
                        <th>Price</th>
                    </tr>
        '''

        secondPart = '''</table></body></html>'''

        invoiceContent = firstPart + invoiceItems + secondPart # merging the header, data and footer

        HTML(string=invoiceContent).write_pdf('your-invoice.pdf',
        stylesheets=[CSS(string='body { background-color: white; font-family: Helvetica, Arial } * { margin: 0; padding: 0; } th { text-align: left } p, h2 { padding: 5px; }')])


with open(('products2.json'), "r", encoding='UTF8') as data_file:
    data = json.load(data_file)

engine = Engine()
InvoiceView(data)