import pdfcrowd
from django.template.loader import get_template
from decouple import config
from micro_auth_service.models import ClientCredentials
from micro_client_service.models import FilingDetails,InvoiceDetails
from micro_admin_service.models import ITR
from datetime import datetime
from EmailServer.email import Mail
import os
from num2words import num2words

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

def generateEngine(obj,invoice_no):
    try:
        template=get_template("invoice.html").render(obj)
        with open(f'media/{invoice_no}'+'.html','wb+') as file:
            file.write(template.encode('UTF-8'))
        #pdf_client = pdfcrowd.HtmlToPdfClient(config('pdfcrowd_username'), config('pdfcrowd_apiKey'))
        pdf_client = pdfcrowd.HtmlToPdfClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')
        pdf_client.convertFileToFile(f'media/{invoice_no}'+'.html', f'media/{invoice_no}'+'.pdf')
        os.remove(f'media/{invoice_no}'+'.html')
        return True
    except:
        pass

#'demo', 'ce544b6ea52a5621fb9d55f8b542d14d'
@parser_classes([JSONParser])
def create(invoice_no,client_id,client_address,request):
    try:
        original_price=float(request.data['original_price'])
        if (request.data).get('discount_percentage'):
            discount_percentage=float(request.data['discount_percentage'])
        else:
            discount_percentage=0
        discount_price=(original_price)-(((original_price)*(discount_percentage))/100)

        client=ClientCredentials.objects.get(client_id=client_id)
        filing_details=FilingDetails.objects.get(client=client_id)
        itr_plan=filing_details.itr_plan

        obj={
            "invoice_no":invoice_no,
            "invoice_date":datetime.strftime(datetime.today(),"%d-%m-%Y"),
            "client_name":client.first_name+" "+client.last_name,
            "client_address":client_address,
            "client_phone":client.phone,
            "client_email":client.email,
            "client_pan":filing_details.pan,
            "itr":itr_plan,
            "original_price":original_price,
            "discount_price":discount_price,
            "price_in_words":num2words(discount_price)
        }
        stat=generateEngine(obj=obj,invoice_no=invoice_no)
        if stat:
            mail_sender = config('SMTP_USERNAME')
            body="We appreciate your trust in our services and the opportunity to assist you with your tax compliance needs. Thank you for choosing our expertise for your ITR filing, and we look forward to serving you in the future.Please find the invoice details below:"
            mail=Mail(
                subject="Invoice",
                body=body,
                mail_sender=mail_sender,
                mail_receiver=client.email
            )
            mail.invoice_send(
                filename=invoice_no+'.pdf',
                client_name=client.first_name+" "+client.last_name
            )
            return True
    except pdfcrowd.Error as why:
        print('why')

@parser_classes([JSONParser])
def createInvoice(request,client_id):
    try:
        client=ClientCredentials.objects.get(client_id=client_id)
        
        if not InvoiceDetails.objects.filter(client=client).exists():
            invoice_no='INV'+str(int(datetime.timestamp(datetime.now())))
            stat=create(invoice_no,client_id,request.data['client_address'],request)
            if stat:
                InvoiceDetails.objects.create(
                        client=client,
                        invoice_number=invoice_no,
                        invoice_date=datetime.strftime(datetime.today(),"%d-%m-%Y"),
                        invoice_filename=invoice_no+'.pdf'
                    )
                return True,{"info":"invoice send","invoice_filename":f'{invoice_no}'+'.pdf',"invoice_number":invoice_no,"invoice_date":datetime.strftime(datetime.today(),"%d-%m-%Y")}
        else:
            return False,{"info":"invoice already exists!"}
    except:
        pass

def deleteInvoice(client_id):
    try:
        client=ClientCredentials.objects.get(client_id=client_id)
        
        if InvoiceDetails.objects.filter(client=client).exists():
            invoice=InvoiceDetails.objects.get(client=client_id)
            os.remove(f'media/{invoice.invoice_filename}')
            invoice.delete()
            return True,{"info":"successfully deleted!"}
        else:
            return False,{"info":"invoice doesn't exists!"}
    except:
        pass