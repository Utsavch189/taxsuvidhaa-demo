from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from micro_auth_service.models import ClientCredentials
from micro_client_service.models import FilingDetails
from datetime import datetime

@parser_classes([JSONParser])
def update_clientFiling(request,client_id):
    try:
        client=ClientCredentials.objects.get(client_id=client_id)
        filing_obj=FilingDetails.objects.filter(client=client)
        if((request.data).get('itr_plan') and len(request.data)==1):
            itr_plan=request.data['itr_plan']
            filing_obj.update(itr_plan=itr_plan)
            return True,{"info":"client itr_type updated!"}
        elif ((request.data).get('filing_date') and len(request.data)==1):
            filing_date=request.data['filing_date']
            filing_obj.update(filing_date=filing_date)
            return True,{"info":"client filing_date updated!"}
        elif ((request.data).get('pan') and len(request.data)==1):
            pan=request.data['pan']
            if FilingDetails.objects.filter(pan=pan).exists():
                return False,{"info":"pan already exists!"}
            filing_obj.update(pan=pan)
            return True,{"info":"client pan updated!"}
        elif ((request.data).get('pan') and (request.data).get('itr_plan') and len(request.data)==2):
            pan=request.data['pan']
            itr_plan=request.data['itr_plan']
            if FilingDetails.objects.filter(pan=pan).exists():
                return False,{"info":"pan already exists!"}
            filing_obj.update(itr_plan=itr_plan,pan=pan,form_submit_date=datetime.strftime(datetime.today(),"%d-%m-%Y"))
            return True,{"info":"client pan and itr_type updated!"}
        elif ((request.data).get('filing_date') and (request.data).get('itr_plan') and len(request.data)==2):
            itr_plan=request.data['itr_plan']
            filing_date=request.data['filing_date']
            filing_obj.update(itr_plan=itr_plan,filing_date=filing_date)
            return True,{"info":"client itr_type and filing_date updated!"}
    except:
        pass
