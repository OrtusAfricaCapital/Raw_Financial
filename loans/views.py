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
from utils import calculations, get_transaction_reseller, xente_payment_MTN, xente_login, constants
import json
import requests
from django.conf import settings
import uuid,  os
import time
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
#from numpy import impt

# Create your views here.

def interest(p,r,t):
    i = (p*r*t)/100
    return i


def request_uid():
    pass



class LoanView(LoginRequiredMixin, ListView):
    model = Loans
    template_name = 'loans/show_loans.html'

@login_required(login_url='login')
def create_loan_view(request, id):
    try:
        borrower = Borrower.objects.get(id=id)
        tn = TrustNetwork.objects.get(id=borrower.tn.id)
        channel = Channel.objects.get(id=tn.channel.id)
        if request.method == 'POST':
            loan_form = LoanForm(request.POST or None)
            if loan_form.is_valid():
                lf = loan_form.save(commit=False)
                lf.borrower = borrower
                lf.interest_rate = tn.MonthlyInterestRate
                loan_amount = loan_form.cleaned_data.get('principal_amount')
                duration = loan_form.cleaned_data.get('loan_duration')
               
                
                LoanRequest.objects.create(
                    channel_id = channel,
                    loan_amount = loan_amount,
                    loan_purpose = "",
                    loan_duration = duration
                )
                lf.save()
                messages.success(request, "successfully created loan request")
                return redirect('loan_borrowed', id=id)
            else:
                loan_form = LoanForm()
                messages.error(request, "oops, something went wrong")
                return redirect('create_loan', id=id)
        else:
            loan_form = LoanForm()
            context = {
                'loan_form':loan_form,
                'borrower':borrower
            }
            return render(request, 'loans/create_loan.html', context)
    except Borrower.DoesNotExist:
        return redirect('loan_borrowed', id=id)


@login_required(login_url='login')
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

@login_required(login_url='login')
def edit_loan_view(request, loan_uid):
    context= {}
    get_loan = Loans.objects.get(loan_uid=loan_uid)
    edit_loan_form = LoansForm(instance=get_loan)
    if request.method == 'POST':
        edit_loan_form = LoansForm(request.POST, instance=get_loan)
        if edit_loan_form.is_valid():
            edit_loan_form.save()
            messages.success(request, "Successfully edited loan")
            return redirect('show_loans')
        else:
            context['edit_loan_form']=edit_loan_form
            messages.error(request, "Opps Field error")
            return render(request, 'loans/edit_loan.html', context)

    else:
        context['edit_loan_form']=edit_loan_form
        
        return render(request, 'loans/edit_loan.html', context)

@login_required(login_url='login')
def delete_loan_view(request, loan_uid):
    get_loan = Loans.objects.get(loan_uid=loan_uid)
    get_loan.delete()
    messages.error(request, "Successfully deleted loan")
    return redirect('show_loans')


@login_required(login_url='login')
def payment_view(request, loan_uuid):
    #get_loan
    get_loan = Loans.objects.get(loan_uid=loan_uuid)
    

    loan_borrowed = Loans.objects.filter(borrower=get_loan.borrower)
    principal_sum = Loans.objects.filter(borrower=get_loan.borrower).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0
    #disburse the credit through xente
    
    context = {}
    payment_form = PaymentForm()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST or None)
        if payment_form.is_valid():
            pf = payment_form.save(commit=False)
            amount = payment_form.cleaned_data.get('amount_paid')
            date = payment_form.cleaned_data.get('when_paid')

            if amount > get_loan.principal_amount:
                messages.error(request, "Loan Amount is above that the loan amount")
                context = {'form':payment_form}
                return render(request, 'loans/create_payment.html', context)
            


            #use xente
            xente_login.get_token(constants.api_key, constants.api_password)
            
            
            #print(r)

            
            #result_method = xente_payment_MTN.create_payment_MTN(amount, get_loan.borrower.phone_number, get_loan.borrower.phone_number,get_loan.borrower.email, get_loan.borrower.phone_number)
            
            url = constants.base_url_payment+"/api/v1/transactions"
            headers={'X-ApiAuth-ApiKey':settings.XENTE_API_KEY, 
                    'X-Date':str(datetime.datetime.now(timezone.utc)), 
                    'X-Correlation-ID':'uuid.uuid4()',
                    'Authorization': "Bearer "+str(os.environ.get('XENTE_TOKEN')),
                    'Content-Type': 'application/json'}
            payload = json.dumps({
                "PaymentProvider": "MTNMOBILEMONEYUG",
                "paymentItem": "MTNMOBILEMONEYUG",
                "amount": amount,
                "message": "Test Transaction",
                "customerId": get_loan.borrower.phone_number,
                "customerPhone": get_loan.borrower.phone_number,
                "customerEmail": get_loan.borrower.email,
                "customerReference": get_loan.borrower.phone_number,
                "metadata": None,
                "batchId": "TestBatchId001",
                "requestId": constants.request_uid,
            })
            result_method = requests.request("POST", url, headers=headers, data=payload)

            if result_method.status_code == 201:
                try:
                    #print(response.json())
                    result = result_method.json()
                    data = result['data']
                    message = data['message']
                    transaction_id = data['transactionId']
                    created_at = data['createdOn']
                    #correlation_id = data['correlationId']
                    
                    context = {
                        'loan_details':get_loan,
                        'form':payment_form,
                        'transaction_id':transaction_id
                    }
                    
                    #Loans.objects.filter(loan_uid=loan_uuid).update(loan_status="Processing")
                    messages.success(request, message)
                    
                    
                    #return redirect('loan_borrowed', id=get_loan.borrower.id)
                    return render(request, 'loans/create_payment.html', context)
                except ValueError:
                    result = result_method.json()
                    message = data['message']
                    code = str(result_method.status_code)
                    messages.error(request, message + code)
                    return redirect('loan_borrowed', id=get_loan.borrower.id)
            else:
                try:
                    result = result_method.json()
                    message = result['message']
                    code = str(result_method.status_code)
                    context = {
                            'loan_borrowed':loan_borrowed,
                            'total_borrowed': principal_sum,
                            'id':get_loan.borrower.id

                        }
                    messages.error(request, message + code),
                    return redirect('loan_borrowed', id=get_loan.borrower.id)
                except ValueError:
                    message = result_method.status_code
                    messages.error(request, message),
                    return redirect('loan_borrowed', id=get_loan.borrower.id)
        else:
            context = {'form':payment_form}
            messages.error(request, "Oops, Field error")
            return render(request, 'loans/create_payment.html', context)
    else:
        context = {
                'loan_details':get_loan,
                'form':payment_form
            }
        return render(request, 'loans/create_payment.html', context)

@login_required(login_url='login')
def payment_status_view(request, transaction_id, loan_uuid):
    payment_form = PaymentForm()
    get_loan = Loans.objects.get(loan_uid=loan_uuid)
    
    loan_borrowed = Loans.objects.filter(borrower=get_loan.borrower)
    principal_sum = Loans.objects.filter(borrower=get_loan.borrower).aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0.0

    xente_login.get_token(constants.api_key, constants.api_password)
    #print(os.environ.get('XENTE_TOKEN'))

    headers={'X-ApiAuth-ApiKey':settings.XENTE_API_KEY, 
                    'X-Date':str(datetime.datetime.now(timezone.utc)), 
                    'X-Correlation-ID':'uuid.uuid4()',
                    'Authorization': "Bearer "+str(os.environ.get('XENTE_TOKEN')),
                    'Content-Type': 'application/json'}
    url_transactions_payment = constants.base_url_payment+"/api/v1/transactions/"+transaction_id+"?pageSize=20&pageNumber=1"

    response = requests.request("GET", url_transactions_payment, headers=headers)

    if response.status_code == 200:
        result = response.json()
        #print(result)
        result_data = result['data']
        status  = result_data['status']
        request_id = result_data['requestReference']
        created_at = result_data['createdOn']
        status_message = result_data['statusMessage']
        #print(result)
        
        if status == "PROCESSING":
            """
            LoanTransactions.objects.create(
                loan_id = get_loan,
                transaction_id = transaction_id,
                request_id = request_id,
                transaction_type = "Deposit",
                trnsaction_status = status,
                transaction_created_on = created_at
            )
            """
            context = {
                        'loan_details':get_loan,
                        'form':payment_form,
                        'transaction_id':transaction_id
                    }
                    
            messages.success(request, status_message),
            return render(request, 'loans/create_payment.html', context)

        elif status == "COMMITTED":
            LoanTransactions.objects.create(
                loan_id = get_loan,
                transaction_id = transaction_id,
                request_id = request_id,
                transaction_type = "Deposit",
                transaction_status = status,
                transaction_created_on = created_at
            )
        
            Payment.objects.create(
                user = request.user,
                loan_id = get_loan,
                borrower_id=get_loan.borrower,
                amount_paid=get_loan.principal_amount,
                when_paid=created_at
            )
            Loans.objects.filter(loan_uid=loan_uuid).update(loan_status="Paid")
            messages.success(request, status_message)
            return redirect('loan_borrowed', id=get_loan.borrower.id)
        elif status == "FAILED":
            messages.success(request, status_message),
            return redirect('loan_borrowed', id=get_loan.borrower.id)
    else:
        try:
            result = response.json()
            message = result['message']
            code = str(response.status_code)
            context = {
                    'loan_borrowed':loan_borrowed,
                    'total_borrowed': principal_sum,
                    'id':get_loan.borrower.id

                }
            messages.error(request, message + code)
            return redirect('loan_borrowed', id=get_loan.borrower.id)
        except ValueError:
           
            code = str(response.status_code)
            messages.error(request, code),
            return redirect('loan_borrowed', id=get_loan.borrower.id)
     
        
    return redirect('loan_borrowed', id=get_loan.borrower.id)

@login_required(login_url='login')
def get_loan_requests(request):
    get_loan_request = LoanRequest.objects.all()
    context = {
        'loan_request':get_loan_request
    }
    return render(request, 'loans/loan_requests.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def give_loan(request, uid):
    try:
        get_loan_request = LoanRequest.objects.get(loan_request_uid=uid)
        loan_borrowed = Borrower.objects.get(channel_borrower_uid=get_loan_request.channel_borrower_uid)

        LoanRequestStatus.objects.filter(loan_id=get_loan_request.id).update(loan_status="approved", loan_status_description="Loan Request has been approved")
        
       
        #disburse the credit through xente
        #response = xente_payment_MTN.create_payment_MTN(get_loan_request.loan_amount, loan_borrowed.phone_number, loan_borrowed.phone_number, loan_borrowed.email, loan_borrowed.phone_number)
        r=xente_login.get_token_reseller('BC52D6E0D7C042308EABBBFD6D2AFB9C', 'Raw#ortus2022')
        #print (r)
        #print(os.environ.get('XENTE_RESELLER_TOKEN'))
        if r:

            url = settings.XENTE_BASE_URL_RESELLER+"/api/v1/transactions"

            request_id = str(uuid.uuid4())
            
            payload = json.dumps({
                "product": "MTNMOBILEMONEYPAYOUTUG_MTNMOBILEMONEYPAYOUTUG",
                "productItem": "MTNMOBILEMONEYPAYOUTUG_MTNMOBILEMONEYPAYOUTUG",
                "amount": get_loan_request.loan_amount,
                "message": "Test Transation from Raw Financial",
                "customerId": '256775022805',
                "customerPhone": '256775022805',
                "customerEmail": loan_borrowed.email,
                "customerReference": '256775022805',
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
                    
                    context = {
                            'loan_request':get_loan_request,
                            'loan_borrowed':loan_borrowed,
                            'loan_status':True,
                            'transaction_id':transaction_id

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
            status_code = r
            context = {
                    'loan_request':get_loan_request,
                    'loan_borrowed':loan_borrowed,
                
                }
            messages.error(request, status_code),
            return render(request, 'loans/loan_request_details.html', context)
        
    except LoanRequest.DoesNotExist:
        pass

@login_required(login_url='login')       
def give_loan_status(request, transaction_id, uid):
    get_loan_request = LoanRequest.objects.get(loan_request_uid=uid)
    loan_borrowed = Borrower.objects.get(channel_borrower_uid=get_loan_request.channel_borrower_uid)

    xente_login.get_token_reseller('BC52D6E0D7C042308EABBBFD6D2AFB9C', 'Raw#ortus2022')

    headers={'X-ApiAuth-ApiKey':settings.XENTE_API_KEY_RESELLER, 
                    'X-Date':str(datetime.datetime.now(timezone.utc)), 
                    'X-Correlation-ID':'uuid.uuid4()',
                    'Authorization': "Bearer "+str(os.environ.get('XENTE_RESELLER_TOKEN')),
                    'Content-Type': 'application/json'}
    url_transactions = constants.base_url_reseller+"/api/v1/transactions/"+transaction_id+"?pageSize=20&pageNumber=1"

    response = requests.request("GET", url_transactions, headers=headers)

    if response.status_code == 200:
        result = response.json()
        result_data = result['data']
        status  = result_data['status']
        status_message = result_data['statusMessage']
        request_id = result_data['requestReference']
        created_at = result_data['createdOn']
        print(result)
        
        if status == "PROCESSING":
            context = {
                    'loan_request':get_loan_request,
                    'loan_borrowed':loan_borrowed,
                    'loan_status':True,
                    'transaction_id':transaction_id
                }
            messages.warning(request, status_message)
            return render(request, 'loans/loan_request_details.html', context)

        elif status == "SUCCESS":
            """
            create_loan=Loans.objects.create(
                    borrower=loan_borrowed,
                    principal_amount=get_loan_request.loan_amount,
                    loan_release_date=datetime.datetime.now(timezone.utc),
                    interest_rate=loan_borrowed.tn.MonthlyInterestRate,
                    loan_duration = get_loan_request.loan_duration,
                    loan_status="Issued")
            """
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
                'loan_status':True,
                'transaction_id':transaction_id
            }
            messages.warning(request, status_message)
            return render(request, 'loans/loan_request_details.html', context)
        elif status == "FAILED":
            context = {
                    'loan_request':get_loan_request,
                    'loan_borrowed':loan_borrowed,
                    'loan_status':True,
                    'transaction_id':transaction_id
                }
            messages.error(request, status_message),
            return render(request, 'loans/loan_request_details.html', context)
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

@login_required(login_url='login')
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
