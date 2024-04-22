from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from micro_auth_service.JWT.jwt_authorization import IsAuthorized,IsTokenValids
from rest_framework import status
from micro_admin_service.services.clientNotes_service import *

import logging
logger=logging.getLogger('mylogger')

@api_view(['POST'])
@permission_classes([IsAuthorized,IsTokenValids])
def update_notes(request,client_id):
    try:
        logger.info('update_notes')
        message,stat=updateNote(request=request,client_id=client_id)
        if stat==200:
            return Response(message,status=status.HTTP_200_OK)
        elif stat==201:
            return Response(message,status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error('update_notes || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthorized,IsTokenValids])
def remove_notes(request,client_id):
    try:
        logger.info('remove_notes')
        message=removeNote(client_id=client_id)
        return Response(message,status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('remove_notes || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthorized,IsTokenValids])
def get_notes(request):
    try:
        logger.info('get_notes')
        data=getNotes()
        return Response({"info":data},status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('get_notes || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)