from django.urls import path

from micro_auth_service.controller.login_views import adminLogin,clientLogin,refresh_token,reset_password
from micro_auth_service.controller.register_views import ClientRegister,is_ClientExists,manualClientRegister
from micro_auth_service.controller.otpVerify_views import ClientOtpVerify


urlpatterns = [
    path('admin/login',adminLogin),
    path('client/login',clientLogin),
    path('collect_newToken/user_id=<str:user_id>&user_type=<str:user_type>',refresh_token),
    path('reset_password',reset_password),
    path('client_register',ClientRegister),
    path('manual_clientregister',manualClientRegister),
    path('client_verify',ClientOtpVerify),
    path('is_clientexists/phone=<str:phone>',is_ClientExists)
]
