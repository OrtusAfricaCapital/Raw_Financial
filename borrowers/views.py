from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.
class BorrowerView(ListView):
    model = Borrower
    template_name = 'borrower/show_borrower.html'

def create_borrower(request):
    context = {}
    b_form = BorrowersForm()
    if request.method == 'POST':
        b_form = BorrowersForm(request.POST or None)
        if b_form.is_valid():
            b_form.save()
            messages.success(request, "successfuly created borrower")
            return redirect('show_borrowers')
        else:
            messages.error(request, "Oops, Field Error")
            return redirect('create_borrower')
    else:
        return render(request, 'borrower/create_borrower.html', context={'borrower_form':b_form})




def create_borrower_view(request, id):
    try:
        trust_network = TrustNetwork.objects.get(id=id)
        context = {}
        if request.method == 'POST':
            b_form = BorrowerForm(request.POST or None)
            if b_form.is_valid():
                b = b_form.save(commit=False)
                b.tn = trust_network
                b.save()
                messages.success(request, "successfuly created borrower")
                return redirect('channel_borrowers', id=id)
            else:
                b_form = BorrowerForm()
                messages.error(request, "Oops, Field Error")
                return redirect('create_borrower')
        else:
            b_form = BorrowerForm()
            return render(request, 'borrower/create_borrower.html', context={'borrower_form':b_form})
    except TrustNetwork.DoesNotExist:
        messages.error(request, "oops, something happened")
        return redirect('channel_borrowers', id=id)



def edit_borrower_view(request, id):
    try:
        get_borrower = Borrower.objects.get(id=id)
        b_form = BorrowersForm(instance=get_borrower)
        if request.method == 'POST':
            b_form = BorrowersForm(request.POST, instance=get_borrower)
            if b_form.is_valid():
                b_form.save()
                messages.success(request, "successfuly edited borrower")
                return redirect('show_borrowers')
            else:
                
                messages.error(request, "Oops, Field Error")
                return redirect('edit_borrower', id=id)
        return render(request, 'borrower/create_borrower.html', context={'borrower_form':b_form})
    except Borrower.DoesNotExist:
        messages.error(request, "oops, Borrower Doesn't Exist")
        return redirect('edit_borrower', id=id)

def delete_view(reqeuest, id):
    get_borrower = Borrower.objects.get(id=id)
    get_borrower.delete()
    return redirect('show_borrowers')





