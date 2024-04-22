from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from micro_auth_service.JWT.jwt_authorization import IsAuthorized,IsTokenValids
from rest_framework import status
from micro_admin_service.services.invoice_service import *

import logging
logger=logging.getLogger('mylogger')

@api_view(['POST'])
@permission_classes([IsAuthorized,IsTokenValids])
def create_invoice(request,client_id):
    try:
        logger.info('create_invoice')
        stat,message=createInvoice(request=request,client_id=client_id)
        if stat:
            return Response(message,status=status.HTTP_200_OK)
        else:
            return Response(message,status=status.HTTP_409_CONFLICT)
    except Exception as e:
        logger.error('create_invoice || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthorized,IsTokenValids])
def delete_invoice(request,client_id):
    try:
        logger.info('delete_invoice')
        stat,message=deleteInvoice(client_id=client_id)
        if stat:
            return Response(message,status=status.HTTP_200_OK)
        else:
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error('delete_invoice || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)