from rest_framework import permissions
import jwt
from rest_framework.exceptions import APIException

from decouple import config

jwt_secret=config('jwt_secret')
jwt_algos=config('jwt_algos')



class IsAuthorized(permissions.BasePermission):

    def has_permission(self,request,view):
        if request.META.get('HTTP_AUTHORIZATION'):
            return True
        else:
           raise UnauthorizedException()
    

class IsTokenValids(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            header= request.META.get('HTTP_AUTHORIZATION')
            token_data = jwt.decode((header.split(' ', 1)[1]), jwt_secret, algorithms=jwt_algos)
            return True
        except Exception as e:
            raise TokenValidException()

class UnauthorizedException(APIException):
    status_code=401
    default_detail = {'info': 'UnAuthorized'}
    default_code="UnAuthorized"

class TokenValidException(APIException):
    status_code=403
    default_detail={'info': 'Token Expired'}
    default_code="Token Expired"