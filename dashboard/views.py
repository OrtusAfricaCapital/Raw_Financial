from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import User
from datetime import datetime, timedelta

from django.db.models import Sum
from wallet.models import *
from loans.models import *
from utils import calculations


# Create your views here.
@login_required(login_url='login')
def index(request):
    transaction = WalletTransactions.objects.all().order_by('-transacted_on')[:5]
    balance = WalletTransactions.objects.aggregate(Sum('amount'))['amount__sum'] or 0.0
    loans_issued = Loans.objects.all().aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0
    loans_due_sum = Loans.objects.filter(loan_release_date__gt=datetime.now()-timedelta(days=30)).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0
    loans_due = Loans.objects.filter(loan_release_date__gt=datetime.now()-timedelta(days=30)).count()

    #npl percentage
    npl_percentage = calculations.percentage_npl_amountlent(loans_due_sum,loans_issued)

    #pl calculation
    amount_paid = 301430000
    pl = calculations.pl(loans_issued, amount_paid)

    pl_percentage = calculations.percentage_pl_amountlent(pl, loans_issued)

    context = {
        'loans_issued':loans_issued,
        'loans_due_sum':loans_due_sum,
        'loans_due':loans_due,
        'transactions':transaction,
        'balance': balance,
        'npl_percent':npl_percentage,
        'pl':pl,
        'pl_percent':pl_percentage,
    }
    return render(request, 'dashboard/home.html', context)
