from django.db import models
from micro_auth_service.models import ClientCredentials

class Notes(models.Model):
    client=models.ForeignKey(ClientCredentials,on_delete=models.CASCADE,related_name='notes')
    note=models.TextField(default="")
    date=models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
        return str(self.client)


class ITR(models.Model):
    itr_type=models.IntegerField(primary_key=True,default=0)
    itr_name=models.CharField(max_length=50,null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
    price_in_words=models.CharField(max_length=50,null=True,blank=True)

    def __str__(self) -> str:
        return self.itr_name

class TransactionDetailsOfClient(models.Model):
    client=models.ForeignKey(ClientCredentials,on_delete=models.CASCADE,related_name='transaction_details')
    transaction_id=models.CharField(primary_key=True,max_length=50,default="")
    transaction_date=models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.transaction_id