from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from micro_auth_service.models import ClientCredentials
from micro_client_service.models import FilingDetails
from micro_admin_service.models import ITR
from decouple import config
from EmailServer.email import Mail
from datetime import datetime

@parser_classes([JSONParser])
def planSelect(request,client_id):
    try:
        pan=request.data['pan']
        itr_plan=int(request.data['itr_plan'])
        client=ClientCredentials.objects.get(client_id=client_id)

        plan=ITR.objects.get(itr_type=itr_plan)
        plan_name=plan.itr_name
        plan_price=plan.price
        
        if(FilingDetails.objects.filter(client=client).exists()):
            return False,{"info":"Already a record exists!"}
        elif(FilingDetails.objects.filter(pan=pan).exists()):
            return False,{"info":"pan number already exists!"}
        else:
            f=FilingDetails(client=client,pan=pan,itr_plan=itr_plan,form_submit_date=datetime.strftime(datetime.today(),"%d-%m-%Y"),filing_date="")
            f.save()
            subject="Plan Selection Successfully"
            body=f"You have successfully registered for {plan_name}(₹{plan_price}/-).Our Tax experts will contact you shortly."
            email=client.email
            mail_sender = config('SMTP_USERNAME')
            mail=Mail(subject=subject,body=body,mail_sender=mail_sender,mail_receiver=email)
            mail.mailWithTemplate(client_name=client.first_name+" "+client.last_name)
            return True,{"info":"Record created!"}
    except Exception as e:
        print(e)
        pass

def isPlanSelected(client_id):
    try:
        client=ClientCredentials.objects.get(client_id=client_id)
        if(FilingDetails.objects.filter(client=client).exists()):
            return {"exist":"true"}
        else:
            return {"exist":"false"}
    except:
        pass