from django import forms
from django.forms import fields
from .models import *

class FinancialInstitutionForm(forms.ModelForm):
    class Meta:
        model = FinancialInstitution
        fields = ('Name','DailyInterestRate','MonthlyInterestRate',
        'EmailAddress','PhoneNumber','VerificationStatus','InstitutionalStatus','Image')
