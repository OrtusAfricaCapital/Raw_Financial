from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import User

from django.db.models import Sum
from wallet.models import *


# Create your views here.
@login_required(login_url='login')
def index(request):
    transaction = WalletTransactions.objects.all().order_by('-transacted_on')[:5]
    balance = WalletTransactions.objects.aggregate(Sum('amount'))['amount__sum'] or 0.0
    context = {
        'transactions':transaction,
        'balance': balance
    }
    return render(request, 'dashboard/home.html', context)
