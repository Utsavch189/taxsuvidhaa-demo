from django.contrib import admin
from .models import Notes,TransactionDetailsOfClient,ITR


admin.site.register(Notes)
admin.site.register(TransactionDetailsOfClient)
admin.site.register(ITR)