import datetime
from datetime import timezone
from email import header
import time
from webbrowser import get

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Sum

from wallet.models import LoanTransactions
from .forms import *
from .models import *
from utils import calculations, xente_payment_MTN, xente_login, constants
import json
import requests
from django.conf import settings
import uuid,  os
#from numpy import impt

# Create your views here.

def interest(p,r,t):
    i = (p*r*t)/100
    return i


def request_uid():
    pass


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

def payment_view(request, loan_uuid):
    #get_loan
    get_loan = Loans.objects.get(loan_uid=loan_uuid)

    loan_borrowed = Loans.objects.filter(loan_uid=loan_uuid)
    principal_sum = Loans.objects.filter(loan_uid=loan_uuid).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0
    #disburse the credit through xente
    
    xente_login.get_token(constants.api_key, constants.api_password)
    response = xente_payment_MTN.create_payment_MTN(get_loan.principal_amount, get_loan.borrower.phone_number, get_loan.borrower.phone_number, get_loan.borrower.email, get_loan.borrower.phone_number)
    

    """
    url = "http://sandbox666353.westeurope.cloudapp.azure.com:9080/api/v1/transactions"

    request_id = str(uuid.uuid4())
    
    payload = json.dumps({
    "PaymentProvider": "MTNMOBILEMONEYUG",
    "paymentItem": "MTNMOBILEMONEYUG",
    "amount": get_loan.principal_amount,
    "message": "Test Transaction from Raw Financial",
    "customerId": get_loan.borrower.phone_number,
    "customerPhone": get_loan.borrower.phone_number,
    "customerEmail": "jasiimwe160@gmail.com",
    "customerReference": get_loan.borrower.phone_number,
    "metadata": None,
    "batchId": "TestBatchId001",
    "requestId": request_id
    })
    headers={'X-ApiAuth-ApiKey':settings.XENTE_API_KEY, 
            'X-Date':str(datetime.datetime.now(timezone.utc)), 
            'X-Correlation-ID':'uuid.uuid4()',
            'Authorization': "Bearer "+str(os.environ.get('XENTE_TOKEN')),
            'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)
    """
    if response.status_code == 201:
        try:
            #print(response.json())
            result = response.json()
            data = result['data']
            request_id = data['requestId']
            message = data['message']
            transaction_id = data['transactionId']
            created_at = data['createdOn']
            #correlation_id = data['correlationId']

            LoanTransactions.objects.create(
                loan_id = get_loan,
                transaction_id = transaction_id,
                request_id = request_id,
                
                transaction_type = "Deposit",
                transaction_created_on = created_at
            )

            Payment.objects.create(
                user = request.user,
                loan_id = get_loan,
                borrower_id=get_loan.borrower,
                amount_paid=get_loan.principal_amount,
                when_paid=datetime.datetime.now(timezone.utc)
            )

            context = {
                    'loan_borrowed':loan_borrowed,
                    'total_borrowed': principal_sum

                }
            messages.success(request, message),
            return render(request, 'channel/loan_borrowed.html', context)
        except ValueError:
            print("something went wrong111")
    else:
        try:
            result = response.json()
            message = result['message']
            context = {
                    'loan_borrowed':loan_borrowed,
                    'total_borrowed': principal_sum

                }
            messages.error(request, message),
            return render(request, 'channel/loan_borrowed.html', context)
        except:
            print(response.status_code)

    context = {
                    'loan_borrowed':loan_borrowed,
                    'total_borrowed': principal_sum

                }
    messages.success(request, "something"),
    return render(request, 'channel/loan_borrowed.html', context)
    """
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
    """

def get_loan_requests(request):
    get_loan_request = LoanRequest.objects.all()
    context = {
        'loan_request':get_loan_request
    }
    return render(request, 'loans/loan_requests.html', context)

def loan_request_details(request, uid):
    try:
        get_loan_request = LoanRequest.objects.get(loan_request_uid=uid)
        borrower = Borrower.objects.get(channel_borrower_uid=get_loan_request.channel_borrower_uid)
        loan_borrowed = Loans.objects.filter(borrower=borrower.id)
        context = {
            'loan_request':get_loan_request,
            'loan_borrowed':loan_borrowed
        }
        return render(request, 'loans/loan_request_details.html', context)
    except LoanRequest.DoesNotExist:
        pass

def give_loan(request, uid):
    try:
        get_loan_request = LoanRequest.objects.get(loan_request_uid=uid)
        loan_borrowed = Borrower.objects.get(channel_borrower_uid=get_loan_request.channel_borrower_uid)

        LoanRequestStatus.objects.filter(loan_id=get_loan_request.id).update(loan_status="approved", loan_status_description="Loan Request has been approved")
        
        
        create_loan = Loans.objects.create(
            borrower=loan_borrowed,
            principal_amount=get_loan_request.loan_amount,
            loan_release_date=datetime.datetime.now(timezone.utc),
            interest_rate=loan_borrowed.tn.MonthlyInterestRate,
            loan_duration = get_loan_request.loan_duration,
            loan_status="Issued"
        )
        
        
        if create_loan:
            #disburse the credit through xente
            #response = xente_payment_MTN.create_payment_MTN(get_loan_request.loan_amount, loan_borrowed.phone_number, loan_borrowed.phone_number, loan_borrowed.email, loan_borrowed.phone_number)
            xente_login.get_token_reseller('11B0199BA7F14827BC3247097002A57D', 'XentE@Test1234')
            #print(os.environ.get('XENTE_RESELLER_TOKEN'))
            url = settings.XENTE_BASE_URL_RESELLER+"/api/v1/transactions"

            request_id = str(uuid.uuid4())
            
            payload = json.dumps({
                "product": "MTNMOBILEMONEYPAYOUTUG_MTNMOBILEMONEYPAYOUTUG",
                "productItem": "MTNMOBILEMONEYPAYOUTUG_MTNMOBILEMONEYPAYOUTUG",
                "amount": get_loan_request.loan_amount,
                "message": "Test Transation from Raw Financial",
                "customerId": get_loan_request.loan_amount,
                "customerPhone": get_loan_request.loan_amount,
                "customerEmail": loan_borrowed.email,
                "customerReference": get_loan_request.loan_amount,
                "metadata": None,
                "batchId": "TestBatchId001",
                "requestId": request_id
                })
            headers={'X-ApiAuth-ApiKey':settings.XENTE_API_KEY_RESELLER, 
                    'X-Date':str(datetime.datetime.now(timezone.utc)), 
                    'X-Correlation-ID':'uuid.uuid4()',
                    'Authorization': "Bearer "+str(os.environ.get('XENTE_RESELLER_TOKEN')),
                    'Content-Type': 'application/json'}

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 201:
                try:
                    #print(response.json())
                    result = response.json()
                    data = result['data']
                    request_id = data['requestId']
                    message = data['message']
                    transaction_id = data['transactionId']
                    created_at = data['createdOn']
                    #correlation_id = data['correlationId']
                    
                    LoanTransactions.objects.create(
                        loan_id = create_loan,
                        transaction_id = transaction_id,
                        request_id = request_id,
                        
                        transaction_type = "Withdraw",
                        transaction_created_on = created_at
                    )

                    
                    
                    context = {
                            'loan_request':get_loan_request,
                            'loan_borrowed':loan_borrowed,

                        }
                    messages.success(request, message),
                    return render(request, 'loans/loan_request_details.html', context)
                except ValueError:
                    print("something went wrong111")
            else:
                try:
                    result = response.json()
                    message = result['message']
                    context = {
                            'loan_request':get_loan_request,
                            'loan_borrowed':loan_borrowed,

                        }
                    messages.error(request, message),
                    return render(request, 'loans/loan_request_details.html', context)
                except:
                    print(response.status_code)
                #print(os.environ.get('XENTE_TOKEN'))
                    
        
        else:
            pass
        
        
        
        context = {
                'loan_request':get_loan_request,
                'loan_borrowed':loan_borrowed,
               
            }
        messages.warning(request, "Loan issued"),
        return render(request, 'loans/loan_request_details.html', context)
        
    except LoanRequest.DoesNotExist:
        pass
        
    

def loan_scoring(request, uid):
    context = {}
    try:
        get_loan_request = LoanRequest.objects.get(loan_request_uid=uid)
        channel_borrower_id = get_loan_request.channel_borrower_uid
        #check loan status
        borrower = Borrower.objects.get(channel_borrower_uid=channel_borrower_id)
        loan_borrowed = Loans.objects.filter(borrower=borrower.id, loan_status="Running")
        tn = TrustNetwork.objects.get(id=borrower.tn.id)
        
        if loan_borrowed:
            context = {
                'status':False,
                'loan_request':get_loan_request
            }
            messages.error(request, "Loan Scoring Failed. The Borrower has a Running Loan")
            return render(request, 'loans/loan_request_details.html', context)

        else:
            if get_loan_request.loan_amount > tn.InstitutionalLimit:
                context = {
                    'status':False,
                    'loan_request':get_loan_request
                }
                messages.error(request, "Loan Scoring Failed. The Institutional Limit has been exceeded")
                return render(request, 'loans/loan_request_details.html', context)
            else:
                #issue Loan and change status for Loan Request
                #LoanRequestStatus.objects.filter(loan_id=get_loan_request.id).update(loan_status="approved", loan_status_description="Loan has been approved")
                context = {
                    'status':True,
                    'loan_request':get_loan_request
                }
                messages.success(request, "Passed Loan Scoring")
                return render(request, 'loans/loan_request_details.html', context)
        
                
        #messages.warning(request, "Still has existing Loan"),
            

    except LoanRequest.DoesNotExist:
        context['loan_request'] = get_loan_request
        return render(request, 'loans/loan_request_details.html', context)
