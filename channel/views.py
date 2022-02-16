from code import interact
from wallet.forms import DepositForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Sum
from .forms import *
from .models import *
from trust_network.models import *
from borrowers.models import *
from loans.models import *
from loans.forms import *
from utils import calculations
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ChannelView(LoginRequiredMixin, ListView):
    model = Channel
    template_name = 'channel/show_channel.html'

@login_required(login_url='login')
def channel_view(request):
    context = {}
    if request.method == 'POST':
        channel_form = ChannelForm(request.POST, request.FILES)
        if channel_form.is_valid():
            channel_form.save()
            messages.success(request, "created channel")
            return redirect('show_channel')
        else:
            channel_form = ChannelForm()
            messages.error(request, channel_form.errors)
            return render(request, 'channel/create_channel.html', context={'channel_form':channel_form})
    else:
        channel_form = ChannelForm()
        return render(request, 'channel/create_channel.html', context={'channel_form':channel_form})

@login_required(login_url='login')
def channel_details(request, id):
    total_loan_amount = 0
    channel_details = get_object_or_404(Channel, pk=id)
    trustnetwork_channel = TrustNetwork.objects.filter(channel=id)
    for tn in trustnetwork_channel:
        borrower = Borrower.objects.filter(tn=tn)
        
        
        for b in borrower:
            loan_amount = Loans.objects.filter(borrower=b).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0
            total_loan_amount = total_loan_amount + loan_amount 
        
    
    intrest_rate = calculations.calculate_intrest(total_loan_amount, 10)
    total_amount = total_loan_amount + intrest_rate

    context = {
        'tn_channel':trustnetwork_channel,
        'channel_details':channel_details,
        'total_loan_amount': total_loan_amount,
        'channel_interest_amount':intrest_rate,
        'total_amount': total_loan_amount + intrest_rate
    }
    return render(request, 'channel/channel_details.html', context)

@login_required(login_url='login')  
def edit_channel_view(request, id):
    get_channel = Channel.objects.get(id=id)
    channel_form = ChannelForm(instance=get_channel)
    if request.method == 'POST':
        channel_form = ChannelForm(request.POST, instance=get_channel)
        if channel_form.is_valid():
            channel_form.save()
            messages.success(request, "Successfully Edited Channel")
            return redirect('show_channel')
        else:
            
            messages.error(request, channel_form.errors)
            return render(request, 'channel/create_channel.html', context={'channel_form':channel_form})
    else:
        
        return render(request, 'channel/create_channel.html', context={'channel_form':channel_form})







def delete_channel(request, id):
    get_channel = Channel.objects.get(id=id)
    get_channel.delete()
    return redirect('show_channel')

def show_borrowers_in_network(request, id):
    borrowers = Borrower.objects.filter(tn=id)
    
    
    
    context = {
        'borrowers':borrowers,
        'id':id,
    }
    return render(request, 'channel/channel_borrower.html', context)

def loan_borrower(request, id):
    loan_borrowed = Loans.objects.filter(borrower=id)
    borrower = Borrower.objects.get(id=id)
    principal_sum = Loans.objects.filter(borrower=id).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0
    interest = calculations.calculate_intrest(principal_sum, borrower.tn.MonthlyInterestRate)

    context = {
        'loan_borrower':loan_borrowed,
        'total_borrowed': principal_sum,
        'interest':interest,
        'total_amount': principal_sum + interest,
        'id':id
    }
    return render(request, 'channel/loan_borrowed.html', context)

def loan_details(request, id):
    loan_borrowed = Loans.objects.filter(loan=id)
    principal_sum = Loans.objects.filter(loan=id).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0


    context = {
        'loan_borrower':loan_borrowed,
        'total_borrowed': principal_sum
    }
    return render(request, 'channel/loan_borrowed.html', context)


def make_payment(request, id):
    loan = Loans.objects.get(borrower=id)
    context = {}
    payment_form = PaymentForm()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST or None)
        if payment_form.is_valid():
            pf = payment_form.save(commit=False)
            pf.user = request.user
            pf.loan_id = loan
            pf.borrower_id = loan.borrower
            pf.save()
            messages.success(request, "Payment successfully logged")
            return redirect('loan_borrowed', id=id)
        else:
            
            context = {'form':payment_form}
            messages.error(request, "Oops, Field error")
            return render(request, 'loans/create_payment.html', context)
    else:
        context = {'form':payment_form}
        return render(request, 'loans/create_payment.html', context)