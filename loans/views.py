from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Sum
from .forms import *
from .models import *
from utils import calculations
#from numpy import impt

# Create your views here.

def interest(p,r,t):
    i = (p*r*t)/100
    return i

class LoanView(ListView):
    model = Loans
    template_name = 'loans/show_loans.html'

def create_loan_view(request, id):
    try:
        borrower = Borrower.objects.get(id=id)
        if request.method == 'POST':
            loan_form = LoanForm(request.POST or None)
            if loan_form.is_valid():
                lf = loan_form.save(commit=False)
                lf.borrower = borrower
                loan_form.save()
                messages.success(request, "Loan Created successfully")
                return redirect('loan_borrowed', id=id)
            else:
                loan_form = LoanForm()
                messages.error(request, "oops, something went wrong")
                return redirect('create_loan', id=id)
        else:
            loan_form = LoanForm()
            return render(request, 'loans/create_loan.html', context={'loan_form':loan_form})
    except Borrower.DoesNotExist:
        return redirect('loan_borrowed', id=id)

def loan_details(request, id):
    loan_borrowed = Loans.objects.get(id=id)
    #principal_sum = Loans.objects.(id=id).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0

    #interest = ((10/100)/30) * loan_borrowed['principal_amount']
    
    #interest = (loan_borrowed.principal_amount*1*10)/100
    interest = calculations.calculate_intrest(loan_borrowed.principal_amount, 10)
    ti = interest+loan_borrowed.principal_amount
    #Compound_interest = loan_borrowed.principal_amount * ((1+10/100)**1 - 1)
    context = {
        'loan_borrower':loan_borrowed,
        'total_borrowed': loan_borrowed.principal_amount,
        'interest':interest,
        'ti': ti
        
    }
    return render(request, 'loans/loan_details.html', context)

def payment_view(request):
    context = {}
    payment_form = PaymentForm()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST or None)
        if payment_form.is_valid():
            pf = payment_form.save(commit=False)
            pf.user = request.user
            pf.save()
            messages.success(request, "Payment successfully logged")
            return redirect('show_payments')
        else:
            
            context = {'form':payment_form}
            messages.error(request, "Oops, Field error")
            return render(request, 'loans/create_payment.html', context)
    else:
        context = {'form':payment_form}
        return render(request, 'loans/create_payment.html', context)

def get_loan_requests(request):
    get_loan_request = LoanRequest.objects.all()
    context = {
        'loan_request':get_loan_request
    }
    return render(request, 'loans/loan_requests.html', context)
