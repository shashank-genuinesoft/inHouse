from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Companies)
admin.site.register(Transactions)
admin.site.register(LedgerMaster)
admin.site.register(transactionAccount)
admin.site.register(GroupMaster)
admin.site.register(Users)
