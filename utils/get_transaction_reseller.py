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
import random
import string
from django.conf import settings


header_date = str(datetime.datetime.now(timezone.utc))
header_correlation_id = 'uuid.uuid4()'
header_content_type = 'application/json'
api_key_reseller = settings.XENTE_API_KEY_RESELLER


def get_trasaction(transaction_id):
    url = constants.base_url_reseller+"/api/v1/transactions/"+transaction_id+"?pageSize=20&pageNumber=1"
    headers_reseller={'X-ApiAuth-ApiKey':api_key_reseller, 
    'X-Date':header_date, 
    'X-Correlation-ID':header_correlation_id, 
    'Content-Type':header_content_type}
    
    response = requests.request("GET", url, headers=headers_reseller)

    return response