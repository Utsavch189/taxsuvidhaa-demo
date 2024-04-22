from django.core.management import call_command
from micro_auth_service.models import OTP
from datetime import datetime

def db_backUp():
  try:
    call_command('dbbackup')
  except:
    pass

def otp_clear():
  try:
    objs=OTP.objects.filter(expiry__lt=(datetime.timestamp(datetime.now())))
    objs.delete()
  except:
    pass