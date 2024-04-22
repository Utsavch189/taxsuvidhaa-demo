from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from micro_client_service.services.extra_service import *

import logging
logger=logging.getLogger('mylogger')

@api_view(['POST'])
def contact(request):
    try:
        logger.info('contact')
        stat=Contact(request=request)
        if stat:
            return Response({"info":"Email sent!"},status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('contact || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def webfootprint(request):
    try:
        logger.info('webfootprint')
        stat,message=footprint(request=request)
        if stat:
            return Response(message,status=status.HTTP_200_OK)
        else:
            return Response(message,status=status.HTTP_200_OK) 
    except Exception as e:
        logger.error('webfootprint || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)