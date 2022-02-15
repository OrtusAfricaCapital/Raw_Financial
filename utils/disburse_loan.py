from utils import calculations, get_transaction_reseller, xente_payment_MTN, xente_login, constants
import json
import requests
from django.conf import settings
import uuid,  os
import datetime
from datetime import timezone



def give_loan(amount, customer_id, email, customer_phone, customer_reference):
    url = settings.XENTE_BASE_URL_RESELLER+"/api/v1/transactions"

    request_id = str(uuid.uuid4())
    
    payload = json.dumps({
        "product": "MTNMOBILEMONEYPAYOUTUG_MTNMOBILEMONEYPAYOUTUG",
        "productItem": "MTNMOBILEMONEYPAYOUTUG_MTNMOBILEMONEYPAYOUTUG",
        "amount": amount,
        "message": "Test Transation from Raw Financial",
        "customerId": customer_id,
        "customerPhone": customer_phone,
        "customerEmail": email,
        "customerReference": customer_reference,
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

            disbursed = True, message, transaction_id, created_at
        except ValueError:
            message = data['message']
            disbursed = False, message
    else:
        try:
            result = response.json()
            message = result['message']
            disbursed = False, message
            
        except:
            message = result['message']
            disbursed = False, message

    return disbursed


def check_status(transaction_id):
    url = settings.XENTE_BASE_URL_RESELLER+"api/v1/transactions/"+transaction_id

    headers={'X-ApiAuth-ApiKey':settings.XENTE_API_KEY_RESELLER, 
            'X-Date':str(datetime.datetime.now(timezone.utc)), 
            'X-Correlation-ID':'uuid.uuid4()',
            'Authorization': "Bearer "+str(os.environ.get('XENTE_RESELLER_TOKEN')),
            'Content-Type': 'application/json'}

    request = requests.request("GET", url, headers=headers, params={'pageSize':20, 'pageNumber':1})

    return print(request.text)