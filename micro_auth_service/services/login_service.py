from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from micro_auth_service.models import *
from micro_auth_service.JWT.jwt import JWT_Builder
from django.contrib.auth.hashers import check_password,make_password
import uuid
from EmailServer.emailserve import sendOTP
from datetime import datetime

def saveRefreshToken(user,refreshToken,user_type):
    if user_type=='admin':
        if(RefreshToken.objects.filter(user_admin=user).exists()):
            RefreshToken.objects.filter(user_admin=user).update(refresh_token=refreshToken)
        else:
            o=RefreshToken(user_admin=user,user_client=None,refresh_token=refreshToken)
            o.save()
    elif user_type=='client':
        if(RefreshToken.objects.filter(user_client=user).exists()):
            RefreshToken.objects.filter(user_client=user).update(refresh_token=refreshToken)
        else:
            o=RefreshToken(user_admin=None,user_client=user,refresh_token=refreshToken)
            o.save()

@parser_classes([JSONParser])
def admin_login(request):
    try:
        username=request.data['email']
        password=request.data['password']
        print(AdminCredentials.objects.filter(username=username).exists())
        if(AdminCredentials.objects.filter(username=username).exists() and check_password(password,AdminCredentials.objects.get(username=username).password)):
                tokens=JWT_Builder({
                    'sub':username
                }).get_token()
                user_instance=AdminCredentials.objects.get(username=username)
                token_pair={"access_token":tokens['access_token'],"refresh_token":tokens['refresh_token']}
                saveRefreshToken(user_instance,tokens['refresh_token'],"admin")
                return True,token_pair
        else:
            return False,{}
    except:
        pass

@parser_classes([JSONParser])
def client_login(request):
    try:
        phone=request.data['phone']
        client_id=uuid.uuid3(uuid.NAMESPACE_DNS,str(phone))
        if(ClientCredentials.objects.filter(client_id=client_id).exists()):

                    tokens=JWT_Builder({
                        'sub':str(client_id),
                        'email':ClientCredentials.objects.get(client_id=client_id).email,
                        'phone':ClientCredentials.objects.get(client_id=client_id).phone,
                        'name':ClientCredentials.objects.get(client_id=client_id).first_name+" "+ClientCredentials.objects.get(client_id=client_id).last_name
                    }).get_token()
                    user_instance=ClientCredentials.objects.get(client_id=client_id)
                    token_pair={"access_token":tokens['access_token'],"refresh_token":tokens['refresh_token']}
                    saveRefreshToken(user_instance,tokens['refresh_token'],"client")
                    return True,token_pair
        else:
             return False,{}
    except:
        pass


def return_validToken_fromRefreshToken(user_id,user_type):
     try:
        if user_type=='admin':
          if(AdminCredentials.objects.filter(username=user_id).exists()):             
                    tokens=JWT_Builder({
                    'sub':user_id
                    }).get_token()
                    token_pair={"info":"new tokens are generated!","access_token":tokens['access_token'],"refresh_token":tokens['refresh_token']}
                    saveRefreshToken(AdminCredentials.objects.get(username=user_id),tokens['refresh_token'],user_type)
                    return True,token_pair
          else:
               return False,{}
        elif user_type=='client':
            if(ClientCredentials.objects.filter(client_id=user_id).exists()):             
                    tokens=JWT_Builder({
                    'sub':user_id
                    }).get_token()
                    token_pair={"info":"new tokens are generated!","access_token":tokens['access_token'],"refresh_token":tokens['refresh_token']}
                    saveRefreshToken(ClientCredentials.objects.get(client_id=user_id),tokens['refresh_token'],user_type)
                    return True,token_pair
            else:
               return False,{}
     except:
          pass

@parser_classes([JSONParser])
def reset_yourPassword(request):
    try:
        if((request.data).get('email') and len(request.data)==1):
            email=request.data['email']
            if(AdminCredentials.objects.filter(username=email).exists()):
                    sendOTP(email=email,user=email)
                    return True,{"info":f"OTP has been sent to {email}"}
            else:
                return False,{"info":f"Email '{email}' is not registered"}
    
        elif((request.data).get('otp') and (request.data).get('email')):
            otp=request.data['otp']
            email=request.data['email']
            if(OTP.objects.filter(otp_id=email).exists()):
                    Otp=OTP.objects.get(otp_id=email)
                    if(float(Otp.expiry)>datetime.timestamp(datetime.now())):
                        if(int(Otp.otp)==int(otp)):
                            Otp.delete()
                            return True,{"info":f"Now reset your password for {email}"}
                        else:
                            return False,{"info":"You have provided an invalid OTP"}
                    else:
                        Otp.delete()
                        return False,{"info":"OTP has been expired! Please click on resend"}         

        elif((request.data).get('new_password') and (request.data).get('email')):
                email=request.data['email']
                user=AdminCredentials.objects.get(username=email)
                new_password=request.data['new_password']
                user.password=make_password(new_password)
                user.save()
                return True,{"info":"Password has been changed successfully"}
    except:
         pass
