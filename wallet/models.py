from pyexpat import model
from django.db import models
from financial_institute.models import *
from channel.models import *
from loans.models import Loans

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


class LoanTransactions(models.Model):
    loan_id = models.ForeignKey(Loans, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    request_id = models.CharField(max_length=100)
    correlation_id = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=200)
    transaction_status = models.CharField(max_length=200)
    transaction_created_on = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.transaction_id
    


    