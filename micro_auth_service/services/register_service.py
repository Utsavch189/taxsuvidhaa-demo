from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from EmailServer.email import Mail
import uuid
from micro_auth_service.models import ClientCredentials
from decouple import config
from datetime import datetime
from micro_client_service.models import FilingDetails
from JsonParser.parser import parse
from micro_admin_service.serializers import ClientSerializer
from micro_admin_service.models import ITR

@parser_classes([JSONParser])
def reg_of_client(request):
    try:
        first_name=request.data['first_name'].strip().capitalize()
        last_name=request.data['last_name'].strip().capitalize()
        email=(request.data['email'].strip()).lower()
        phone=request.data['phone']
        client_id=uuid.uuid3(uuid.NAMESPACE_DNS,str(phone).strip())
        
        if (ClientCredentials.objects.filter(client_id=client_id).exists() and ClientCredentials.objects.filter(email=email).exists() and ClientCredentials.objects.filter(phone=phone).exists()):
            return False,{"info":"can't register!"}
        
        o=ClientCredentials(client_id=client_id,first_name=first_name,last_name=last_name,phone=phone,email=email,already_called=False,registered_date=datetime.strftime(datetime.today(),"%d-%m-%Y"),registered_timestamp=(datetime.timestamp(datetime.now())*1000))
        o.save()
        subject="Successfully Registered!"
        body="Welcome to TaxSuvidhaa! Our experts are thrilled to have you on board.Our Expert Team will be in touch with you shortly to provide personalized guidance tailored to your tax needs. Get ready for a hassle-free and rewarding tax experience. Stay tuned for the expert support that awaits you!"
        mail_sender = config('SMTP_USERNAME')
        mail=Mail(subject=subject,body=body,mail_sender=mail_sender,mail_receiver=email)
        mail.mailWithTemplate(client_name=first_name+" "+last_name)
        client=ClientCredentials.objects.filter(client_id=client_id)
        data=parse(ClientSerializer(client,many=True).data)
        return True,{"info":"registered","client":data}
    except Exception as e:
        print(e)
        pass

def client_existance(phone):
    client_id=uuid.uuid3(uuid.NAMESPACE_DNS,str(phone))
    if(ClientCredentials.objects.filter(phone=phone).exists()):
        email=ClientCredentials.objects.filter(phone=phone).values('email')[0]['email']
        return {"info":"Account exists!","exist_status":'true','email':email,'client_id':client_id}
    else:
        return {"info":"Account doesn't exists!","exist_status":'false','client_id':client_id}
    
@parser_classes([JSONParser])
def manualRegister(request):
    try:
        if not((request.data).get('client_first_name')and(request.data).get('client_last_name')and(request.data).get('email')and(request.data).get('phone')and(request.data).get('pan')and(request.data).get('itr')):
            return False,{"info":"supply all the details!"}
        else:
            client_id=uuid.uuid3(uuid.NAMESPACE_DNS,str(request.data['phone']).strip())
            
            if ClientCredentials.objects.filter(client_id=client_id).exists() or ClientCredentials.objects.filter(email=request.data['email']).exists() or FilingDetails.objects.filter(pan=request.data['pan']).exists() or ClientCredentials.objects.filter(phone=request.data['phone']).exists():
                return False,{"info":"duplicate records"}
            
            c=ClientCredentials(client_id=client_id,first_name=request.data['client_first_name'].strip(),last_name=request.data['client_last_name'].strip(),phone=request.data['phone'],email=(request.data['email'].strip()).lower(),already_called=False,registered_date=datetime.strftime(datetime.today(),"%d-%m-%Y"),registered_timestamp=(datetime.timestamp(datetime.now())*1000))
            c.save()

            plan=ITR.objects.get(itr_type=request.data['itr'])
            plan_name=plan.itr_name
            plan_price=plan.price
            f=FilingDetails(client=c,pan=request.data['pan'],itr_plan=request.data['itr'],form_submit_date=datetime.strftime(datetime.today(),"%d-%m-%Y"),filing_date="")
            f.save()

            subject="Successfully Registered With Plan Selection "
            body=f"Welcome to TaxSuvidhaa! You have successfully registered for {plan_name}(₹{plan_price}/-).Our Tax experts will contact you shortly."
            mail_sender = config('SMTP_USERNAME')
            mail=Mail(subject=subject,body=body,mail_sender=mail_sender,mail_receiver=request.data['email'].strip())
            mail.mailWithTemplate(client_name=request.data['client_first_name'].strip()+" "+request.data['client_last_name'].strip())

            client=ClientCredentials.objects.filter(client_id=client_id)
            data=parse(ClientSerializer(client,many=True).data)
            return True,{"info":"client registration done!","data":data}
    except Exception as e:
        print(e)


