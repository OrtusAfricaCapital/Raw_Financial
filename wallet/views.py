
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *
from django.db.models import Sum

from django.urls import reverse_lazy


# Create your views here.

def show_wallet(request):
    df = DepositForm()
    wf = WithdrawForm()
    transactions = WalletTransactions.objects.all()
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
