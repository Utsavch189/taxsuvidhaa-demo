from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from micro_auth_service.JWT.jwt_authorization import IsAuthorized,IsTokenValids
from rest_framework import status
from micro_admin_service.services.clientDetails_service import allClientsWithBasicInfo,register_vs_footprints,allClientsAllDetailsWithPagination,allClientsWithAllDetails,client_alreadyphone_update

import logging
logger=logging.getLogger('mylogger')

@api_view(['GET'])
@permission_classes([IsAuthorized,IsTokenValids])
def clientinfo(request):
    try:
        logger.info('clientinfo')
        data=allClientsWithBasicInfo()
        return Response({"data":data},status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('clientinfo || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthorized,IsTokenValids])
def countings(request):
    try:
        logger.info('countings')
        pie_data,line_data=register_vs_footprints()
        return Response({"piedata":pie_data,"linedata":line_data},status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('countings || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthorized,IsTokenValids])
def clientAllDetailsPaginated(request,page):
    try:
        logger.info('clientAllDetailsPaginated')
        data,total_clients=allClientsAllDetailsWithPagination(page=page)
        return Response({"data":data,"total_data":total_clients},status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('clientAllDetailsPaginated || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthorized,IsTokenValids])
def clientAllDetails(request):
    try:
        logger.info('clientAllDetails')
        data,total_clients=allClientsWithAllDetails()
        return Response({"data":data,"total_data":total_clients},status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('clientAllDetails || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PATCH'])
@permission_classes([IsAuthorized,IsTokenValids])
def update_already_called(request,client_id):
    try:
        logger.info('update_already_called')
        stat=client_alreadyphone_update(client_id=client_id)
        if stat:
            return Response({"info":"updated!"},status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('update_already_called || '+getattr(e, 'message', repr(e)))
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 