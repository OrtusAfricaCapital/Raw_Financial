from django import forms
from .models import *

class TrustNetworkForm(forms.ModelForm):
    class Meta:
        model = TrustNetwork
        fields = ('channel','Name','InstitutionalLimit','RevolvingLimit','DailyInterestRate',
        'MonthlyInterestRate','Logo','CreatedBy','TrustNetworkCategory',
        'RequiresApproval','RequiredApproval','Domains')
