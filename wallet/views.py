
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.shortcuts import get_object_or_404


from .forms import *
from .models import *
from django.db.models import Sum

from django.urls import reverse_lazy
import requests
from django.conf import settings
import json
import uuid
import datetime
from datetime import timezone
import os
from utils import xente_login


header_api_key = settings.XENTE_API_KEY
header_date = str(datetime.datetime.now(timezone.utc))
header_correlation_id = 'uuid.uuid4()'
header_content_type = 'application/json'
header_token = str(os.environ.get('XENTE_TOKEN'))

headers={'X-ApiAuth-ApiKey':header_api_key, 
    'X-Date':header_date, 
    'X-Correlation-ID':header_correlation_id,
    'Authorization': "Bearer "+header_token, 
    'Content-Type':header_content_type}


# Create your views here.

def show_wallet(request):
    df = DepositForm()
    wf = WithdrawForm()
    transactions = LoanTransactions.objects.all()
    wallet_sum = WalletTransactions.objects.aggregate(Sum('amount'))['amount__sum'] or 0.0
    context = {
        'df_form':df,
        'wf_form':wf,
        'dep':wallet_sum,
        'transactions':transactions,
    }
    return render(request, 'wallet/wallet.html', context)


def deposit_view(request):
    if request.method == 'POST':
        df = DepositForm(request.POST or None)
        if df.is_valid():
            df.save()
            transactions = WalletTransactions.objects.create(
                transaction_type= "Deposit", 
                amount = df.cleaned_data['amount'],
                party = str(df.cleaned_data['investor']),
            )
            transactions.save()
            messages.success(request, "Deposit successfull")
            return redirect('show_wallet')
        else:
            df = DepositForm()
            messages.error(request, "something went wrong")
            return redirect('show_wallet')
    else:
        
        df = DepositForm()
        return render(request, 'wallet/wallet.html', context={'df_form':df})


def withdraw_view(request):
    if request.method == 'POST':
        wf = WithdrawForm(request.POST or None)
        if wf.is_valid():
            wf.save()
            transactions = WalletTransactions.objects.create(
                transaction_type= "Withdraw", 
                amount = (wf.cleaned_data['amount']) * -1,
                party = str(wf.cleaned_data['channel']),
            )
            transactions.save()
            messages.success(request, "Withdraw successfull")
            return redirect('show_wallet')
        else:
            wf = WithdrawForm()
            messages.error(request, "something went wrong")
            return redirect('show_wallet')
    else:
        wf = WithdrawForm()
        return render(request, 'wallet/wallet.html', context={'wf_form':wf})


class Transaction(ListView):
    model = WalletDeposit
    template_name = 'wallet/wallet.html'


def login_sandbox_api(request):
    
    response = xente_login.get_token(settings.XENTE_API_KEY, settings.XENTE_PASSWORD)
    print(response)
    context = {
           
            "message":response,
            "token":os.environ.get('XENTE_TOKEN')
        }
    
    return render(request, 'wallet/xente_sandbox.html', context)
    

def create_transaction(request):
    pass


    

    