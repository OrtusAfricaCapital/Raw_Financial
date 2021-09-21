from django.db import models
from financial_institute.models import *
from channel.models import *

# Create your models here.
class WalletDeposit(models.Model):
    investor = models.ForeignKey(FinancialInstitution, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    deposited_when = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.investor)

class WalletWithdraw(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    withdrew_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.channel)

class WalletTransactions(models.Model):
    transaction_type = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)
    party = models.CharField(max_length=200)
    transacted_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_type
    