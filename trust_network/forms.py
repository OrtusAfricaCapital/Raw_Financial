from django import forms
from django.db.models.query import QuerySet
from .models import *
from channel.models import Channel

class TrustNetworkForm(forms.ModelForm):
    
    
    
    class Meta:
        model = TrustNetwork
        fields = ('channel','Name','InstitutionalLimit','RevolvingLimit','DailyInterestRate',
        'MonthlyInterestRate','Logo','TrustNetworkCategory',
        'RequiresApproval','RequiredApproval','Domains')
