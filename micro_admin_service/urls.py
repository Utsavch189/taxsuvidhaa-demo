from django.urls import path
#from .views import *
from micro_admin_service.controller.clientDetails_views import clientinfo,countings,clientAllDetailsPaginated,clientAllDetails,update_already_called
from micro_admin_service.controller.clientFiling_views import update_filing
from micro_admin_service.controller.clientNotes_views import update_notes,remove_notes,get_notes
from micro_admin_service.controller.invoice_views import create_invoice,delete_invoice
from micro_admin_service.controller.transacion_views import update_transactionDetails 

urlpatterns = [
    path('clientinfo',clientinfo),
    path('countings',countings),
    path('clientAllDetailsPaginated/page=<int:page>',clientAllDetailsPaginated),
    path('clientAllDetails',clientAllDetails),
    path('already_called/client_id=<str:client_id>',update_already_called),
    path('update_filing/client_id=<str:client_id>',update_filing),
    path('update_notes/client_id=<str:client_id>',update_notes),
    path('remove_notes/client_id=<str:client_id>',remove_notes),
    path('get_notes',get_notes),
    path('create_invoice/client_id=<str:client_id>',create_invoice),
    path('delete_invoice/client_id=<str:client_id>',delete_invoice),
    path('update_transactionDetails/client_id=<str:client_id>',update_transactionDetails)
]
