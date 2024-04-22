import requests
from decouple import config

api_key=config('SMS_KEY')

class SendSms:
    def __init__(self,number,otp):
        self.otp=otp
        self.header={
            "authorization":api_key,
            "Content-Type":"application/json"
        }
        self.number=number
        self.url="https://www.fast2sms.com/dev/bulkV2"

    def send(self):
        body={
            "route" : "otp",
            "sender_id" : "TaxSuvidhaa",
            "message" : "TaxSuvidha OTP Verification",
            "variables_values" : self.otp,
            "flash" : 0,
            "numbers" : self.number,
        }
        requests.post(url=self.url,headers=self.header,json=body)

