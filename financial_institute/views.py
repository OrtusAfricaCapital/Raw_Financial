from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class FIView(LoginRequiredMixin, ListView):
    model = FinancialInstitution
    template_name = 'fi/show_fi.html'

@login_required(login_url='login')
def create_fi_view(request):
    context = {}
    if request.method == 'POST':
        fi_form = FinancialInstitutionForm(request.POST, request.FILES)
        if fi_form.is_valid():
            fi_form.save()
            messages.success(request, "Financial Institution created successfully")
            return redirect('show_fi')
        else:
            fi_form = FinancialInstitutionForm()
            messages.error(request, "something went wrong")
    else:
        fi_form = FinancialInstitutionForm()
        return render(request, 'fi/create_fi.html',context={'fi_form':fi_form})


@login_required(login_url='login')
def investor_details_view(request, id):
    investor = get_object_or_404(FinancialInstitution, pk=id)
    context = {
        'investor_details':investor
    }
    return render(request, 'fi/investor_details.html', context)