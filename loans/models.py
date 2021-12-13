from django.db import models
from django.db.models.constraints import BaseConstraint
from django.db.models.enums import Choices
from borrowers.models import * 
import random
# Create your models here.
LOAN_PRODUCT = (
    ('Business Loan', 'Business Loan'),
    ('Student Loan', 'Student Loan')
)
DISBURSED_BY = (
    ('Cash','Cash'),
    ('Cheque', 'Cheque'),
)

LOAN_STATUS = (
    ('received', 'received'),
    ('pending', 'pending'),
    ('approved','approved'),
    ('rejected','rejected'),
    
)

def loan_rand():
    rand = random.randint(1000,9000)
    return "LR-"+str(rand)

def payment_rand():
    rand = random.randint(1000,9000)
    return "LP-"+str(rand)


class Loans(models.Model):
    #loan_product = models.CharField(max_length=100, choices=LOAN_PRODUCT)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    #disbursed_by = models.CharField(max_length=100, choices=DISBURSED_BY)
    principal_amount = models.IntegerField()
    loan_release_date = models.DateTimeField()
    interest_rate = models.FloatField()
    loan_duration = models.IntegerField()
    

    def __str__(self):
        return self.loan_product


class LoanRequest(models.Model):
    loan_request_uid = models.CharField(max_length=20, default=loan_rand, editable=False)
    channel_borrower_uid = models.CharField(max_length=200)
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE)
    loan_amount = models.IntegerField()
    loan_purpose = models.TextField()
    loan_duration = models.IntegerField()
    loan_request_date = models.DateField(blank=True, null=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.loan_request_uid

class LoanRequestStatus(models.Model):
    loan_id = models.ForeignKey(LoanRequest, related_name="loan_request", on_delete=models.CASCADE)
    loan_status = models.CharField(max_length=50, choices=LOAN_STATUS, default="received")
    loan_status_description = models.TextField()
    created_at = models.DateField(auto_now=True)

    def __str__ (self):
        return str(self.loan_id)

    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=20, default=payment_rand)
    loan_id = models.ForeignKey(Loans, on_delete=models.CASCADE)
    borrower_id = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    when_paid = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id




    
