from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from micro_auth_service.models import ClientCredentials
from micro_admin_service.models import Notes
from micro_admin_service.serializers import ClientNote
from JsonParser.parser import parse

@parser_classes([JSONParser])
def updateNote(request,client_id):
    try:
        client=ClientCredentials.objects.get(client_id=client_id)
        note=request.data['note']
        date=request.data['date']
        if(Notes.objects.filter(client=client).exists()):
            Notes.objects.filter(client=client).update(note=note,date=date)
            return {"info":"note updated!"},200
        else:
            n=Notes(client=client,note=note,date=date)
            n.save()
            return {"info":"note created!"},201
    except:
        pass

def removeNote(client_id):
    try:
        note=Notes.objects.get(client=client_id)
        note.delete()
        return {"info":"note removed!"}
    except:
        pass

def getNotes():
    try:
        q=ClientCredentials.objects.all().order_by('client_id')
        data=parse(ClientNote(q,many=True).data)
        return data
    except:
        pass