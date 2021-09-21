from django import forms
from .models import *


class LoanForm(forms.ModelForm):
    class Meta:
        model=Loans
        fields = ('loan_product','borrower','disbursed_by','principal_amount','loan_release_date','interest_rate','loan_duration')