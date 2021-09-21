from django import forms
from django.forms import fields
from .models import *
from wallet.models import *


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ('ChannelName','Logo','WebHook','EmailAddress','PhoneNumber',
        'ShortDescription','LongDescription','DeactivatedOn','ApiKey')

class WithdrawForm(forms.ModelForm):
    class Meta:
        model = WalletWithdraw
        fields = ('channel','amount')