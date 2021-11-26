from django import forms
from .models import *


class LoanForm(forms.ModelForm):
    class Meta:
        model=Loans
        fields = ('principal_amount','loan_release_date','interest_rate','loan_duration')

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount_paid','when_paid')