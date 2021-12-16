from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
class TrustNetworkView(ListView):
    model = TrustNetwork
    template_name = 'tn/show_tn.html'

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


    