from micro_auth_service.models import OTP
from datetime import datetime,timedelta
from decouple import config
from .email import Mail


def saveOTP(user,otp):
    if(OTP.objects.filter(otp_id=user).exists()):
        print('hi')
        obj=OTP.objects.get(otp_id=user)
        obj.otp=otp
        obj.expiry=datetime.timestamp(datetime.now()+timedelta(minutes=3))
        obj.save()
    else:
        print('hio')
        o=OTP(otp_id=user,otp=otp,expiry=datetime.timestamp(datetime.now()+timedelta(minutes=3)))
        o.save()


def sendOTP(email,user):
        try:
            otp=int(str(datetime.timestamp(datetime.now())).replace('.','')[-4:])
            if(len(str(otp))==3):
                otp=int(str(otp)+'0')
            elif(len(str(otp))==2):
                otp=int(str(otp)+'06')
            subject='OTP From TaxSuvidha'
            body=f'Please verify your account with OTP : {otp} within 3 minutes!'
            mail_sender = config('SMTP_USERNAME')
            saveOTP(user,otp)
            mail=Mail(subject,body,mail_sender,email)
            mail.mailWithTemplate("User")
        except:
            pass