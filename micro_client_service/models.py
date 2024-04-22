from django.db import models
from micro_auth_service.models import ClientCredentials

class FootPrints(models.Model):
    footprint=models.CharField(max_length=20,null=True,blank=True,unique=True)
    date=models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
        return self.footprint
    class Meta:
        indexes=[
            models.Index(fields=['date'])
        ]

class FilingDetails(models.Model):
    client=models.ForeignKey(ClientCredentials,on_delete=models.CASCADE,related_name='details')
    pan=models.CharField(max_length=10,primary_key=True,default="")
    itr_plan=models.CharField(max_length=50,null=True,blank=True)
    form_submit_date=models.CharField(max_length=20,null=True,blank=True)
    filing_date=models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
        return str(self.client)
    
class InvoiceDetails(models.Model):
    client=models.ForeignKey(ClientCredentials,on_delete=models.CASCADE,related_name='invoice_details')
    invoice_number=models.CharField(max_length=50,primary_key=True,default="")
    invoice_date=models.CharField(max_length=20,null=True,blank=True)
    invoice_filename=models.CharField(max_length=30,null=True,blank=True)
    def __str__(self):
        return str(self.client)