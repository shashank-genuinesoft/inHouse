import enum
from django.db import models
import datetime
from django.conf import settings
from django.contrib.auth.models import(AbstractBaseUser, BaseUserManager, PermissionsMixin)

PLAFFECT_CHOICE=(
                    ("YES","YES"),
                    ("NO","NO")
                )
                
class Companies(models.Model):
    company_id=models.AutoField(primary_key=True)
    company_name=models.CharField(max_length=255)
    company_address=models.CharField(max_length=500)
    tax_number=models.CharField(max_length=100)
    commercial_year=models.CharField(max_length=100)
    registration_date=models.DateField(default=datetime.date.today, blank=True)
    company_email=models.EmailField(unique=True)
    mobile_number=models.CharField(max_length=20)
    password=models.CharField(max_length=900)
    last_login=models.DateTimeField(blank=True,null=True)
    isVerified = models.BooleanField(blank=False, default=False)
    otp = models.IntegerField(null=True,blank=True)
    activation_key = models.CharField(max_length=150,blank=True,null=True)
    user_secret_key = models.CharField(max_length=500,null=True,blank=True)

class Users(models.Model):
    user_id=models.AutoField(primary_key=True)
    company_id=models.ForeignKey(Companies,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    mobile_number=models.CharField(max_length=20)
    password=models.CharField(max_length=255)
    permission_view=models.CharField(max_length=10,choices=PLAFFECT_CHOICE)
    permission_create=models.CharField(max_length=10,choices=PLAFFECT_CHOICE)
    permission_update=models.CharField(max_length=10,choices=PLAFFECT_CHOICE)
    permission_delete=models.CharField(max_length=10,choices=PLAFFECT_CHOICE)
    
    
class LedgerMaster(models.Model):
    ledger_master_id=models.AutoField(primary_key=True)
    company_id=models.ForeignKey(Companies,on_delete=models.CASCADE)
    ledger_name= models.CharField(max_length=255)
    group_under=models.ForeignKey("GroupMaster",on_delete=models.CASCADE)

class transactionAccount(models.Model):
    account_id=models.AutoField(primary_key=True)
    transaction_id=models.ForeignKey("Transactions",on_delete=models.CASCADE,null=True,blank=True, related_name="accounts")
    account_name=models.CharField(max_length=255)
    account_debit_amount=models.IntegerField(default=0)
    account_credit_amount=models.IntegerField(default=0)
    

class Transactions(models.Model):
    transaction_id=models.AutoField(primary_key=True)
    company_id=models.ForeignKey(Companies,on_delete=models.CASCADE)
    user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True)
    transaction_name=models.CharField(max_length=255)
    voucher_number=models.IntegerField()
    remarks=models.CharField(max_length=1000)
    transaction_date=models.DateField()
    created_at=models.DateField(default=datetime.date.today, blank=True)

class GroupMaster(models.Model):
    group_master_id=models.AutoField(primary_key=True)
    company_id=models.ForeignKey(Companies,on_delete=models.CASCADE)
    group_name=models.CharField(max_length=255)
    is_default_group=models.BooleanField(default=False)
    group_under=models.ForeignKey("GroupMaster",on_delete=models.CASCADE)
    group_nature=models.CharField(max_length=255)
    pl_affect=models.CharField(max_length=10,choices=PLAFFECT_CHOICE)

    

        
