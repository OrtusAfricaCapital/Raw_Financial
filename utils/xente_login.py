import os
import datetime
from datetime import timezone
from django.conf import settings
import json
import uuid
import pytz
import time
import requests



api_key = settings.XENTE_API_KEY
api_key_reseller = settings.XENTE_API_KEY_RESELLER
api_password = settings.XENTE_PASSWORD
base_url_payment = settings.XENTE_BASE_URL_PAYMENT

base_url_reseller = settings.XENTE_BASE_URL_RESELLER

#header variables
header_api_key = settings.XENTE_API_KEY
header_date = str(datetime.datetime.now(pytz.timezone(settings.TIME_ZONE)))
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

#@background(schedule=300)
def get_token(api_key, api_password):

    payload = json.dumps({'apiKey':api_key, 'password':api_password})
    headers={'X-ApiAuth-ApiKey':header_api_key, 
        'X-Date':str(datetime.datetime.now(timezone.utc)), 
        'X-Correlation-ID':header_correlation_id, 
        'Content-Type':header_content_type}
    url = base_url_payment+'/api/v1/Auth/login'
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code != 200:
        result = False
    else:
        response = response.json()
        os.environ['XENTE_TOKEN'] = response['token']
        time = 300
        result=True

        print(response)


    
        

    return result

def get_token_reseller(api_key, api_password):
    payload = json.dumps({'apiKey':api_key, 'password':api_password})
    url = base_url_reseller+'/api/v1/Auth/login?includeRefereshToken=true'
    headers_reseller={'X-ApiAuth-ApiKey':api_key_reseller, 
        'X-Date':header_date, 
        'X-Correlation-ID':header_correlation_id, 
        'Content-Type':header_content_type}
    response = requests.request("POST", url, data=payload, headers=headers_reseller)
    if response.status_code == 200:
        response_data = response.json()
        result = True
        os.environ['XENTE_RESELLER_TOKEN'] = response_data['token']
        os.environ['REFRESH_XENTE_TOKEN'] = response_data['refreshToken']
    else:
        result = False
        print(response.text)

    return result

