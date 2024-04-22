from django.db import models

class AdminCredentials(models.Model):
    username=models.CharField(max_length=100,primary_key=True,default="")
    phone=models.CharField(max_length=15,blank=True,null=True,unique=True)
    password=models.CharField(max_length=350,null=True,blank=True)

    def __str__(self) -> str:
        return f"Admin : {self.username}"
    
class ClientCredentials(models.Model):
    client_id=models.CharField(max_length=100,primary_key=True,default="")
    first_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    phone=models.CharField(max_length=15,blank=True,null=True,unique=True)
    email=models.CharField(max_length=50,blank=True,null=True,unique=True)
    already_called=models.BooleanField(default=False)
    registered_timestamp=models.BigIntegerField(null=True,blank=True)
    registered_date=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        indexes=[
            models.Index(fields=['phone','email','registered_date'])
        ]

class RefreshToken(models.Model):
    user_admin=models.ForeignKey(AdminCredentials,null=True,blank=True,on_delete=models.CASCADE)
    user_client=models.ForeignKey(ClientCredentials,null=True,blank=True,on_delete=models.CASCADE)
    refresh_token=models.CharField(max_length=555,null=True,blank=True)

    def __str__(self):
        if(self.user_admin):
            return str(self.user_admin)
        elif(self.user_client):
            return str(self.user_client)
        else:
            return ""
        
    class Meta:
        indexes=[
            models.Index(fields=['user_admin','user_client'])
        ]
    
class OTP(models.Model):
    otp_id=models.CharField(max_length=100,primary_key=True,default="")
    otp=models.CharField(max_length=4,null=True,blank=True)
    expiry=models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.otp
    
    class Meta:
        indexes=[
            models.Index(fields=['otp'])
        ]    
