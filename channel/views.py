from wallet.forms import DepositForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.
class ChannelView(ListView):
    model = Channel
    template_name = 'channel/show_channel.html'

def channel_view(request):
    context = {}
    if request.method == 'POST':
        channel_form = ChannelForm(request.POST)
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
    if request.method == 'POST':
        df = WithdrawForm(request.POST or None)
        if df.is_valid():
            d = df.save(commit=False)
            d.channel = channel_details
            df.save()
            messages.success(request, "account credited successfully")
            return redirect('channel_details')
        else:
            df = WithdrawForm()
            messages.error(request, 'something went wrong')
    else:
        df = WithdrawForm()
        return render(request, 'channel/channel_details.html', context={'channel_details':channel_details, 'wf_form':df})


