from datetime import date
from unittest import result
from urllib import response
from utils import constants, xente_login
from datetime import timezone
import datetime
import os
import json
import requests
import uuid
from django.conf import settings


def create_payment_MTN(amount, customer_id, customer_phone, customer_email, customer_reference):
    result = xente_login.get_token(constants.api_key, constants.api_password)
    if result:
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
            "customerId": customer_id,
            "customerPhone": customer_phone,
            "customerEmail": customer_email,
            "customerReference": customer_reference,
            "metadata": None,
            "batchId": "TestBatchId001",
            "requestId": constants.request_uid
        })
        response = requests.request("POST", url, headers=headers, data=payload)
    else:
        response = "Couldn't Login"
    
  
    return response
          

    
    
   

        
        
        
   
