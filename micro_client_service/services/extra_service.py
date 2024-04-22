from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from decouple import config
from EmailServer.email import Mail
from micro_client_service.models import FootPrints
from datetime import datetime

@parser_classes([JSONParser])
def Contact(request):
    try:
        client_name=request.data['client_name']
        client_email=request.data['client_email']
        client_phone=request.data['client_phone']
        client_message=request.data['client_message']
        target_email=request.data['target_email']
        subject=f"Taxsuvidhaa. Message from {client_name} Ph. {client_phone} Email. {client_email}"
        mail=Mail(subject,client_message,config('EMAIL_HOST_USER'),target_email)
        mail.send()
        return True
    except:
        pass

def footprint(request):
    try:
        user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip_address:
            ip = user_ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            if(FootPrints.objects.filter(footprint=str(ip)).exists()):
                return False,{"info":"foot print exists"}
            else:
                f=FootPrints(footprint=str(ip),date=datetime.strftime(datetime.today(),"%d-%m-%Y"))
                f.save()
                return True,{"info":"foot print stored"}
    except:
        pass