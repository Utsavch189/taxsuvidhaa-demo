from rest_framework import serializers
from micro_auth_service.models import ClientCredentials
from micro_client_service.models import FilingDetails,InvoiceDetails
from micro_auth_service.models import ClientCredentials
from .models import Notes,TransactionDetailsOfClient

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=('note','date','client')

class TransactionDetailsOfClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=TransactionDetailsOfClient
        fields=('transaction_id','transaction_date','client')

class FilingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=FilingDetails
        fields=('pan','itr_plan','form_submit_date','filing_date')

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=InvoiceDetails
        fields=('invoice_number','invoice_date','invoice_filename')

class ClientSerializer(serializers.ModelSerializer):
    details=FilingDetailsSerializer(many=True)
    notes=NoteSerializer(many=True)
    invoice_details=InvoiceSerializer(many=True)
    transaction_details=TransactionDetailsOfClientSerializer(many=True)
    class Meta:
        model=ClientCredentials
        fields=('client_id','first_name','last_name','phone','email','already_called','registered_date','details','notes','invoice_details','transaction_details')

class ClientBasicInfo(serializers.Serializer):
    client_id=serializers.CharField()
    phone=serializers.CharField()
    email=serializers.CharField()
    already_called=serializers.BooleanField()
    class Meta:
        model=ClientCredentials
        read_only_fields=['client_id','phone','email','already_called']



class ClientNote(serializers.Serializer):
    notes=NoteSerializer(many=True)
    class Meta:
        model=ClientCredentials
        fields=('notes')    