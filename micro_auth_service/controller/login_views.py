from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from micro_auth_service.services.login_service import *
from micro_auth_service.JWT.jwt_authorization import IsAuthorized,IsTokenValids

import logging
logger=logging.getLogger('mylogger')

@api_view(['POST'])
def adminLogin(request):
        try:
            logger.info('adminLogin')
            stat,tokens=admin_login(request=request)
            if stat:
                   return Response(tokens,status=status.HTTP_200_OK)
            else:
                 return Response({"info":"Wrong Email or Password"},status=status.HTTP_400_BAD_REQUEST)  
            
        except Exception as e:
                logger.error('adminLogin || '+getattr(e, 'message', repr(e))) 
                return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def clientLogin(request):
        try: 
            logger.info('clientLogin')
            stat,tokens=client_login(request=request)
            if stat:
                   return Response(tokens,status=status.HTTP_200_OK)
            else:
                 return Response({"info":"Wrong Credentials"},status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
                logger.error('clientLogin || '+getattr(e, 'message', repr(e))) 
                return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@permission_classes([IsAuthorized,IsTokenValids])
def refresh_token(request,user_id,user_type):
    try: 
        logger.info('refresh_token')
        stat,tokens=return_validToken_fromRefreshToken(user_id=user_id,user_type=user_type)
        if stat:
              return Response(tokens,status=status.HTTP_200_OK)
        else:
            return Response({"info":"invalid user"},status=status.HTTP_400_BAD_REQUEST)  
        
    except Exception as e:
        logger.error('refresh_token || '+getattr(e, 'message', repr(e))) 
        return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)   


@api_view(['POST'])
def reset_password(request):
    try:
        logger.info('reset_password')
        stat,message=reset_yourPassword(request=request)
        if stat:
             return Response(message,status=status.HTTP_200_OK)
        else:
             return Response(message,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error('reset_password || '+getattr(e, 'message', repr(e)))


