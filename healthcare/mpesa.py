import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

class Credentials:
    consumer_key='IrxrHnxGmnsyndodKPVYjG8pus8huriQqSqDPNVadJQD30Yg'
    consumer_secret='MyfcKchufBr7jpzx8jiZpsdOGK2sLFVGRsmXnGAoSrMf2hXq5pw3MmCXSzPUXKW5'
    apiurl='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

class AccessToken:
    request= requests.get(Credentials.apiurl, auth=HTTPBasicAuth(Credentials.consumer_key, Credentials.consumer_secret))
    access_token=json.loads(request.text)['access_token']

class Password:
    timestamp= datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode='174379'
    passkey='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    to_encode= shortcode + passkey + timestamp
    encoded_password= base64.b64encode(to_encode.encode())
    decoded_password=encoded_password.decode('utf-8')

