import os
import datetime
from datetime import timezone
from django.conf import settings
import json
import uuid

import requests



api_key = settings.XENTE_API_KEY
api_password = settings.XENTE_PASSWORD
base_url = settings.XENTE_BASE_URL

request_uid = str(uuid.uuid4)

#header variables
header_api_key = settings.XENTE_API_KEY
header_date = str(datetime.datetime.now(timezone.utc))
header_correlation_id = 'uuid.uuid4()'
header_content_type = 'application/json'
header_token = str(os.environ.get('XENTE_TOKEN'))


headers={'X-ApiAuth-ApiKey':header_api_key, 
    'X-Date':header_date, 
    'X-Correlation-ID':header_correlation_id,
    'Authorization': "Bearer "+header_token,
    'Content-Type': 'application/json'}