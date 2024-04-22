from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from micro_auth_service.JWT.jwt_authorization import IsAuthorized,IsTokenValids
from rest_framework import status
from micro_admin_service.services.clientFiling_service import update_clientFiling

import logging
logger=logging.getLogger('mylogger')

@api_view(['PATCH'])
@permission_classes([IsAuthorized,IsTokenValids])
def update_filing(request,client_id):
    try:
        logger.info('update_filing')
        stat,message=update_clientFiling(request=request,client_id=client_id)
        if stat:
            return Response(message,status=status.HTTP_200_OK)
        else:
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error('update_filing || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)