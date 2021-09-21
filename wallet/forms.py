from django import forms
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm


class DepositForm(forms.ModelForm):
    class Meta:
        model = WalletDeposit
        fields = ('investor','amount')



class WithdrawForm(forms.ModelForm):
    class Meta:
        model = WalletWithdraw
        fields = ('channel','amount')

class depositForm(BSModalModelForm):
    class Meta:
        model = WalletDeposit
        fields = ['investor','amount',]
