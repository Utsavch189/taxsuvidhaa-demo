from rest_framework.decorators import parser_classes
import uuid
from datetime import datetime
from rest_framework.parsers import JSONParser
from micro_auth_service.models import OTP
from EmailServer.emailserve import sendOTP
from SmsServer.otpSave import sendsms

@parser_classes([JSONParser])
def otp_send_phone(request):
    phone=request.data['phone']
    client_id=uuid.uuid3(uuid.NAMESPACE_DNS,str(phone))
    otp=int(str(datetime.timestamp(datetime.now())).replace('.','')[-4:])
    if(len(str(otp))==3):
        otp=int(str(otp)+'0')
    elif(len(str(otp))==2):
        otp=int(str(otp)+'06')
    sendsms(client_id=client_id,phone=phone,otp=otp)
    return True,{"info":f"OTP has been sent to {phone}"}

@parser_classes([JSONParser])
def otp_send_email(request):
    email=request.data['email']
    client_id=uuid.uuid3(uuid.NAMESPACE_DNS,email)
    sendOTP(email,client_id)
    return True,{"info":f"OTP has been sent to {email}"}

@parser_classes([JSONParser])
def check_otp_phone(request):
    phone=request.data['phone']
    otp=request.data['otp']
    client_id=uuid.uuid3(uuid.NAMESPACE_DNS,str(phone))
    if(OTP.objects.get(otp_id=client_id)):
        obj=OTP.objects.get(otp_id=client_id)
        if(int(obj.otp)==int(otp) and float(obj.expiry))>datetime.timestamp(datetime.now()):
            obj.delete()
            return True,{"info":"Verification done!"}
        elif (int(obj.otp)!=int(otp) and float(obj.expiry))>datetime.timestamp(datetime.now()):
            return False,{"info":"Wrong OTP!"}
        else:
            obj.delete()
            return False,{"info":"Invalid OTP!"}
        
@parser_classes([JSONParser])       
def check_otp_email(request):
    email=request.data['email']
    otp=request.data['otp']
    client_id=uuid.uuid3(uuid.NAMESPACE_DNS,email)
    print(client_id)
    if(OTP.objects.filter(otp_id=client_id).exists()):
        obj=OTP.objects.get(otp_id=client_id)
        print(obj)
        if(int(obj.otp)==int(otp) and float(obj.expiry))>datetime.timestamp(datetime.now()):
            print('1')
            obj.delete()
            return True,{"info":"Verification done!"}
        elif (int(obj.otp)!=int(otp) and float(obj.expiry))>datetime.timestamp(datetime.now()):
            print('2')
            return False,{"info":"Wrong OTP!"}
        else:
            print('3')
            obj.delete()
            return False,{"info":"Invalid OTP!"}
    else:
        return False,{"info":"Invalid OTP!"}

@parser_classes([JSONParser]) 
def verify(request):
    try:
        
        if((request.data).get('phone') and len(request.data)==1):
            stat,message=otp_send_phone(request=request)   
            return stat,message
        elif((request.data).get('email') and len(request.data)==1):
            stat,message=otp_send_email(request=request)
            return stat,message
        
        elif((request.data).get('phone') and (request.data).get('otp') and len(request.data)==2):
            stat,message=check_otp_phone(request=request)
            return stat,message
        elif((request.data).get('email') and (request.data).get('otp') and len(request.data)==2):
            stat,message=check_otp_email(request=request)
            return stat,message
    except Exception as e:
        print(e)
        pass