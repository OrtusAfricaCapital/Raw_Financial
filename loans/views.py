from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Sum
from .forms import *
from .models import *
#from numpy import impt

# Create your views here.



class LoanView(ListView):
    model = Loans
    template_name = 'loans/show_loans.html'

def create_loan_view(request):
    if request.method == 'POST':
        loan_form = LoanForm(request.POST or None)
        if loan_form.is_valid():
            loan_form.save()
            messages.success(request, "Loan Created successfully")
            return redirect('show_loans')
        else:
            loan_form = LoanForm()
            messages.error(request, "oops, something went wrong")
            return redirect('create_loan')
    else:
        loan_form = LoanForm()
        return render(request, 'loans/create_loan.html', context={'loan_form':loan_form})

def loan_details(request, id):
    loan_borrowed = Loans.objects.filter(id=id)
    principal_sum = Loans.objects.filter(id=id).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0

    #interest = ((10/100)/30) * loan_borrowed['principal_amount']

    context = {
        'loan_borrower':loan_borrowed,
        'total_borrowed': principal_sum,
        
    }
    return render(request, 'loans/loan_details.html', context)
