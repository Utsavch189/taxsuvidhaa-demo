from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from micro_auth_service.JWT.jwt_authorization import IsAuthorized,IsTokenValids
from rest_framework import status
from micro_client_service.services.planSelection_service import *

import logging
logger=logging.getLogger('mylogger')

@api_view(['POST'])
@permission_classes([IsAuthorized,IsTokenValids])
def plan_selection(request,client_id):  
    try:
        logger.info('plan_selection')
        stat,message=planSelect(request=request,client_id=client_id)
        if stat:
            return Response(message,status=status.HTTP_200_OK)
        else:
           return Response(message,status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        logger.error('plan_selection || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthorized,IsTokenValids])
def is_plan_selected(request,client_id):
    try:
        logger.info('is_plan_selected')
        message=isPlanSelected(client_id=client_id)
        return Response(message,status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('is_plan_selected || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
