from .sms import SendSms
from micro_auth_service.models import OTP
from datetime import datetime,timedelta

def saveotp(otp,client_id):
    try:
        if(OTP.objects.get(otp_id=client_id)):
            obj=OTP.objects.get(otp_id=client_id)
            obj.otp=otp
            obj.expiry=datetime.timestamp(datetime.now()+timedelta(minutes=3))
            obj.save()
        else:
            o=OTP(otp_id=client_id,otp=otp,expiry=datetime.timestamp(datetime.now()+timedelta(minutes=1)))
            o.save()
    except:
         pass

def sendsms(client_id,phone,otp):
    try:
       
       sms_instance=SendSms(number=phone,otp=otp)
       saveotp(otp,client_id)
       sms_instance.send()
    except:
        pass