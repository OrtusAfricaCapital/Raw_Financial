from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(WalletWithdraw)
admin.site.register(WalletDeposit)
admin.site.register(WalletTransactions)
admin.site.register(LoanTransactions)
