import requests
from config import FAST2SMS_KEY

def send_sms(phone, message):

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "q",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": phone
    }

    headers = {
        "authorization": FAST2SMS_KEY
    }

    return requests.post(url, data=payload, headers=headers).json()