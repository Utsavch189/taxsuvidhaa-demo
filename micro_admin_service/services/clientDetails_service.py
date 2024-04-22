from micro_auth_service.models import ClientCredentials
from JsonParser.parser import parse
from micro_admin_service.serializers import ClientBasicInfo,ClientSerializer
from datetime import datetime,timedelta
from micro_client_service.models import FootPrints
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def concat(a,b):
    return {**a,**b}

def allClientsWithBasicInfo():
    try:
        q=ClientCredentials.objects.filter(already_called=False).order_by('-registered_timestamp')
        data=parse(ClientBasicInfo(q,many=True).data)
        return data
    except:
        pass

def register_vs_footprints():
    try:
        pie_data=[{"name":"registrations","value":ClientCredentials.objects.count()},{"name":"visits","value":FootPrints.objects.count()}]          
        today=datetime.today()
        dates=[datetime.strftime(today-timedelta(days=5),"%d-%m-%Y"),datetime.strftime(today-timedelta(days=4),"%d-%m-%Y"),datetime.strftime(today-timedelta(days=3),"%d-%m-%Y"),datetime.strftime(today-timedelta(days=2),"%d-%m-%Y"),datetime.strftime(today-timedelta(days=1),"%d-%m-%Y"),datetime.strftime(today,"%d-%m-%Y")]
        line_data=[]
        for date in dates:
            if(FootPrints.objects.filter(date=date).exists()):
                data={"day":date,"visit":FootPrints.objects.filter(date=date).count()}
            else:
                data={"day":date,"visit":0}
            if(ClientCredentials.objects.filter(registered_date=date).exists()):
                data=concat(a=data,b={"registrations":ClientCredentials.objects.filter(registered_date=date).count()})
            else:
                data=concat(a=data,b={"registrations":0})
            line_data.append(data)
        return pie_data,line_data
    except:
        pass

def allClientsAllDetailsWithPagination(page):
    q=ClientCredentials.objects.all().order_by('client_id')
    paginator=Paginator(q,10)
    try:
        query=paginator.page(page)
    except PageNotAnInteger:
        query=paginator.page(1)
    except EmptyPage:
        query=paginator.page(paginator.num_pages)
    data=parse(ClientSerializer(query,many=True).data)
    return data,ClientCredentials.objects.count()

def allClientsWithAllDetails():
    try:
        q=ClientCredentials.objects.all().order_by('client_id')
        data=parse(ClientSerializer(q,many=True).data)
        return data,ClientCredentials.objects.count()
    except:
        pass

def client_alreadyphone_update(client_id):
    try:
        client=ClientCredentials.objects.get(client_id=client_id)
        client.already_called=True
        client.save()
        return True
    except:
        pass