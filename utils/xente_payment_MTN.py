from unittest import result
from urllib import response
from utils import constants, xente_login
import json
import requests


def create_payment_MTN(amount, customer_id, customer_phone, customer_email, customer_reference):
    
    #xente_login.get_token(constants.api_key, constants.api_password)

    url = constants.base_url_payment+"/api/v1/transactions"
    headers=constants.headers
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
    
  
    return response
          

    
    
   

        
        
        
   
