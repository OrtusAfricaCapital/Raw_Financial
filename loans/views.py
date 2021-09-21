from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .forms import *
from .models import *

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
