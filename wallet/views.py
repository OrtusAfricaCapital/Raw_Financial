
#from statistics import correlation
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
from utils import xente_login, constants


header_api_key = settings.XENTE_API_KEY_RESELLER
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
    subscription_id = settings.SUBSCRIPTION_ID
    account_id = settings.ACCOUNT_ID_RESELLER
    account_id_payment = settings.ACCOUNT_ID_PAYMENTS
    correlation_id = str(uuid.uuid4())
    balance = 0
    transaction_data = []
    #get credit fund
    
    xente_login.get_token_reseller('BC52D6E0D7C042308EABBBFD6D2AFB9C', 'Raw#ortus2022')
    #print (r)
    #print(os.environ.get('XENTE_RESELLER_TOKEN'))

    url = settings.XENTE_BASE_URL_RESELLER+"/api/v1/Accounts/"+account_id+"/"+subscription_id+"/Balances"
    url_transactions = settings.XENTE_BASE_URL_RESELLER+"/api/v1/transactions/"
    headers={'X-ApiAuth-ApiKey':settings.XENTE_API_KEY_RESELLER, 
                    'X-Date':str(datetime.datetime.now(timezone.utc)), 
                    'X-Correlation-ID':correlation_id,
                    'Authorization': "Bearer "+str(os.environ.get('XENTE_RESELLER_TOKEN')),
                    'Content-Type': 'application/json'}

    response = requests.request("GET", url, headers=headers)
    transactions_result  = requests.request("GET", url_transactions, headers=headers, params={'pageSize':20, 'pageNumber':1})

    print (response)
    print(transactions_result)
    #print(response)

    if response.status_code == 200 and transactions_result.status_code == 200:
        result = response.json()
        transaction_result_data = transactions_result.json()
        transaction_data = transaction_result_data['data']['transactions']
        
        data = result['data']
        balance = data['balance']
        #wallet_info = data['wallets']
        #status = wallet_info['status_info']
        context = {
            
            'dep':balance,
            'transactions':transaction_data,
        }
        return render(request, 'wallet/wallet.html', context)
    
    

    context = {
        
        'dep':balance,
        'transactions':transaction_data,
    }
    return render(request, 'wallet/wallet.html', context)

    #get money collected
    
        
    
def get_wallet_collections_view(request):
    
    principal_sum = Loans.objects.all().aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0
    transactions = LoanTransactions.objects.all()
    wallet_sum = WalletTransactions.objects.aggregate(Sum('amount'))['amount__sum'] or 0.0
    subscription_id = settings.SUBSCRIPTION_ID
    account_id = settings.ACCOUNT_ID_RESELLER
    account_id_payment = settings.ACCOUNT_ID_PAYMENTS
    correlation_id = str(uuid.uuid4())
    balance_payment = 0
    xente_login.get_token(constants.api_key, constants.api_password)
    #print(rr)
    #print(os.environ.get('XENTE_TOKEN'))

    headers_payment={'X-ApiAuth-ApiKey':settings.XENTE_API_KEY, 
                    'X-Date':str(datetime.datetime.now(timezone.utc)), 
                    'X-Correlation-ID':correlation_id,
                    'Authorization': "Bearer "+str(os.environ.get('XENTE_TOKEN')),
                    'Content-Type': 'application/json'}

    url_payments = constants.base_url_payment+"/api/v1/Accounts/"+account_id_payment
    url_transactions = constants.base_url_payment+"/api/v1/transactions/"
    result_method = requests.request("GET", url_payments, headers=headers_payment)
    transactions_result  = requests.request("GET", url_transactions, headers=headers_payment, params={'pageSize':20, 'pageNumber':1})
    if result_method.status_code == 200 and transactions_result.status_code == 200:
        result = result_method.json()
        transaction_result_data = transactions_result.json()
        transaction_data = transaction_result_data['data']['transactions']
        #transactions = transaction_data['transactions']
        payload = result['data']
        balance_payment = payload['balance']

        context = {
            'total_loan': principal_sum,
            'collected_amount':balance_payment,
            'balance':principal_sum-balance_payment,
            'transactions':transaction_data,
        }
        return render(request, 'wallet/wallet_collections.html', context)
        

    context = {
            'total_loan': principal_sum,
            'collected_amount':balance_payment,
            'balance':principal_sum-balance_payment,
            'error_message':"Wallet off line, Please refresh",
            
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


    

    