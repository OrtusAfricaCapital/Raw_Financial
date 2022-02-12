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
#base_url = settings.XENTE_BASE_URL
base_url_payment = settings.XENTE_BASE_URL_PAYMENT

base_url_reseller = settings.XENTE_BASE_URL_RESELLER

request_uid = str(uuid.uuid4())

time = 300

#header variables
header_api_key = settings.XENTE_API_KEY
header_date = str(datetime.datetime.now(timezone.utc))
header_correlation_id = 'uuid.uuid4()'
header_content_type = 'application/json'
header_token = str(os.environ.get('XENTE_TOKEN'))

header_reseller_token = str(os.environ.get('XENTE_RESELLER_TOKEN'))


headers={'X-ApiAuth-ApiKey':header_api_key, 
    'X-Date':header_date, 
    'X-Correlation-ID':header_correlation_id,
    'Authorization': "Bearer "+header_token,
    'Content-Type': 'application/json'}


headers_reseller={'X-ApiAuth-ApiKey':header_api_key, 
    'X-Date':header_date, 
    'X-Correlation-ID':header_correlation_id,
    'Authorization': "Bearer "+header_reseller_token,
    'Content-Type': 'application/json'}