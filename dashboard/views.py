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
    loans_due_sum = Loans.objects.filter(loan_release_date__lt=datetime.now()).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0
    loans_due = Loans.objects.filter(loan_due_date__lt=datetime.now()).count()
    amount_paid = Payment.objects.all().aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0.0

    #npl percentage
    if loans_due_sum == 0 and loans_issued == 0:

        npl_percentage = 0
        pl = 0
        pl_percentage = 0

    else:
        npl_percentage = calculations.percentage_npl_amountlent(loans_due_sum,loans_issued)
        pl = calculations.pl(loans_issued, amount_paid)
        pl_percentage = calculations.percentage_pl_amountlent(pl, loans_issued)


    #pl calculation
    

    

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
