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

# Create your views here.
class ChannelView(ListView):
    model = Channel
    template_name = 'channel/show_channel.html'

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
            messages.error(request, "something went wrong")
            return redirect('create_channel')
    else:
        channel_form = ChannelForm()
        return render(request, 'channel/create_channel.html', context={'channel_form':channel_form})

def channel_details(request, id):
    channel_details = get_object_or_404(Channel, pk=id)
    trustnetwork_channel = TrustNetwork.objects.filter(channel=id)
    context = {
        'tn_channel':trustnetwork_channel,
        'channel_details':channel_details,
    }
    return render(request, 'channel/channel_details.html', context)
    
    


def show_borrowers_in_network(request, id):
    borrowers = Borrower.objects.filter(tn=id)
    
    
    
    context = {
        'borrowers':borrowers,
    }
    return render(request, 'channel/channel_borrower.html', context)

def loan_borrower(request, id):
    loan_borrowed = Loans.objects.filter(borrower=id)
    principal_sum = Loans.objects.filter(borrower=id).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0


    context = {
        'loan_borrower':loan_borrowed,
        'total_borrowed': principal_sum
    }
    return render(request, 'channel/loan_borrowed.html', context)