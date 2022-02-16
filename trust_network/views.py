from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Sum

from borrowers.models import Borrower
from loans.models import Loans
from .models import *
from .forms import *
from utils import calculations
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class TrustNetworkView(LoginRequiredMixin, ListView):
    model = TrustNetwork
    template_name = 'tn/show_tn.html'

@login_required(login_url='login')
def create_tn_view(request):
    context = {}
    if request.method == 'POST':
        tn_form = TrustNetworkForm(request.POST)
        if tn_form.is_valid():
            tn = tn_form.save(commit=False)
            tn.CreatedBy = request.user
            tn.save()
            messages.success(request, "Successfully created Trust Network")
            return redirect('show_trustnetwork')
        else:
            tn_form = TrustNetworkForm()
            messages.error(request, "something went wrong")
            return redirect('create_trustnetwork')
    else:
        tn_form = TrustNetworkForm()
        return render(request, 'tn/create_tn.html', context={'tn_form':tn_form})



@login_required(login_url='login')
def edit_tn_view(request, id):
    get_tn = TrustNetwork.objects.get(id=id)
    if request.method == 'POST':
        tn_form = TrustNetworkForm(request.POST, instance=get_tn)
        if tn_form.is_valid():
            tn = tn_form.save(commit=False)
            tn.CreatedBy = request.user
            tn.save()
            messages.success(request, "Successfully Edited Trust Network")
            return redirect('show_trustnetwork')
        else:
            tn_form = TrustNetworkForm(instance=get_tn)
            messages.error(request, "something went wrong")
            return redirect('edit_trustnetwork')
    else:
        tn_form = TrustNetworkForm(instance=get_tn)
        return render(request, 'tn/edit_tn.html', context={'tn_form':tn_form})

@login_required(login_url='login')
def tn_details_view(request, id):
    total_loan_amount = 0
    get_tn = TrustNetwork.objects.get(id=id)
    get_borrower = Borrower.objects.filter(tn=id)

    for borrower in get_borrower:
        loan_amount = Loans.objects.filter(borrower=borrower).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0
        total_loan_amount = total_loan_amount + loan_amount 

    intrest_rate = calculations.calculate_intrest(total_loan_amount, 10)

    context = {
        'tn_details':get_tn,
        'borrower_details':get_borrower,
        'total_loan_amount':total_loan_amount,
        'channel_interest_amount':intrest_rate,
        'total_amount': total_loan_amount + intrest_rate
        
    }
    return render(request, 'tn/tn_details.html', context)

def delete_trust_network(request, id):
    get_tn = TrustNetwork.objects.get(id=id)
    
    get_tn.delete()
    
    messages.warning(request, "Successfully deleted Trust Network")
    return redirect('show_trustnetwork')





    