from django.db import models
from django.db.models.constraints import BaseConstraint
from django.db.models.enums import Choices
from borrowers.models import * 
# Create your models here.
LOAN_PRODUCT = (
    ('Business Loan', 'Business Loan'),
    ('Student Loan', 'Student Loan')
)
DISBURSED_BY = (
    ('Cash','Cash'),
    ('Cheque', 'Cheque'),
)


class Loans(models.Model):
    loan_product = models.CharField(max_length=100, choices=LOAN_PRODUCT)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    disbursed_by = models.CharField(max_length=100, choices=DISBURSED_BY)
    principal_amount = models.IntegerField()
    loan_release_date = models.DateTimeField()
    interest_rate = models.FloatField()
    loan_duration = models.IntegerField()

    def __str__(self):
        return self.loan_product
