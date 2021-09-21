from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.
class BorrowerView(ListView):
    model = Borrower
    template_name = 'borrower/show_borrower.html'

def create_borrower_view(request):
    context = {}
    if request.method == 'POST':
        b_form = BorrowerForm(request.POST or None)
        if b_form.is_valid():
            b_form.save()
            messages.success(request, "successfuly created borrower")
            redirect('show_borrowers')
        else:
            b_form = BorrowerForm()
            messages.error(request, "oops, something happened")
            redirect('create_borrower')
    else:
        b_form = BorrowerForm()
        return render(request, 'borrower/create_borrower.html', context={'borrower_form':b_form})
