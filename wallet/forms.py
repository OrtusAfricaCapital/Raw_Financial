from django import forms
from .models import *



class DepositForm(forms.ModelForm):
    class Meta:
        model = WalletDeposit
        fields = ('investor','amount')



class WithdrawForm(forms.ModelForm):
    class Meta:
        model = WalletWithdraw
        fields = ('channel','amount')


