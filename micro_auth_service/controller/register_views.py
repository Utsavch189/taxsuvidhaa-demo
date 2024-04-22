from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from micro_auth_service.JWT.jwt_authorization import IsAuthorized,IsTokenValids
from rest_framework import status
from micro_auth_service.services.register_service import *

import logging
logger=logging.getLogger('mylogger')

@api_view(['POST'])
def ClientRegister(request):
    try:
        logger.info('ClientRegister')
        stat,message=reg_of_client(request=request)
        if stat:
            return Response(message,status=status.HTTP_201_CREATED)
        else:
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error('ClientRegister || '+getattr(e, 'message', repr(e))) 
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def is_ClientExists(request,phone):
    try:
        logger.info('is_ClientExists') 
        message=client_existance(phone=phone)
        return Response(message,status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('is_ClientExists || '+getattr(e, 'message', repr(e))) 
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthorized,IsTokenValids])
def manualClientRegister(request):
     try:
          stat,message=manualRegister(request=request)
          if stat:
              return Response(message,status=status.HTTP_200_OK)
          else:
              return Response(message,status=status.HTTP_400_BAD_REQUEST)
     except:
          pass 