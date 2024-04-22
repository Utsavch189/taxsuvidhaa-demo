from django.contrib import admin
from .models import *

admin.site.register(AdminCredentials)
admin.site.register(RefreshToken)
admin.site.register(OTP)
admin.site.register(ClientCredentials)