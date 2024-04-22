from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from micro_auth_service.services.otpVerify_service import verify

import logging
logger=logging.getLogger('mylogger')

@api_view(['POST'])
def ClientOtpVerify(request):
    try:
        logger.info('ClientOtpVerify') 
        stat,message=verify(request=request)
        if stat:
             return Response(message,status=status.HTTP_200_OK)
        else:
             return Response(message,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
           logger.error('ClientOtpVerify || '+getattr(e, 'message', repr(e))) 
           return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)