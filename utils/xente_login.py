import os
import datetime
from datetime import timezone
from django.conf import settings
import json
import uuid

import requests

api_key = settings.XENTE_API_KEY
api_key_reseller = settings.XENTE_API_KEY_RESELLER
api_password = settings.XENTE_PASSWORD
base_url_payment = settings.XENTE_BASE_URL_PAYMENT

base_url_reseller = settings.XENTE_BASE_URL_RESELLER

#header variables
header_api_key = settings.XENTE_API_KEY
header_date = str(datetime.datetime.now(timezone.utc))
header_correlation_id = 'uuid.uuid4()'
header_content_type = 'application/json'




headers={'X-ApiAuth-ApiKey':header_api_key, 
    'X-Date':header_date, 
    'X-Correlation-ID':header_correlation_id, 
    'Content-Type':header_content_type}

headers_reseller={'X-ApiAuth-ApiKey':api_key_reseller, 
    'X-Date':header_date, 
    'X-Correlation-ID':header_correlation_id, 
    'Content-Type':header_content_type}   

def get_token(api_key, api_password):

    payload = json.dumps({'apiKey':api_key, 'password':api_password})
    header = headers
    url = base_url_payment+'/api/v1/Auth/login'
    response = requests.request("POST", url, data=payload, headers=header)
    if response.status_code == 200:
        response = response.json()
        result = True
        os.environ['XENTE_TOKEN'] = response['token']

    
        

    return response

def get_token_reseller(api_key, api_password):
    payload = json.dumps({'apiKey':api_key, 'password':api_password})
    url = base_url_reseller+'/api/v1/Auth/login?includeRefereshToken=true'
    header = headers_reseller
    response = requests.request("POST", url, data=payload, headers=header)
    if response.status_code == 200:
        response = response.json()
        result = True
        os.environ['XENTE_RESELLER_TOKEN'] = response['token']
        os.environ['REFRESH_XENTE_TOKEN'] = response['refreshToken']
    else:
        result = False
        print(response)

    return result

