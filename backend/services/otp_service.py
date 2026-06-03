import random
import time

otp_store = {}
resend_store = {}

OTP_EXPIRY = 300
RESEND_TIME = 60

def generate_otp(phone):
    otp = str(random.randint(100000, 999999))

    otp_store[phone] = {
        "otp": otp,
        "expires": time.time() + OTP_EXPIRY
    }

    return otp

def verify_otp(phone, otp):

    if phone not in otp_store:
        return False

    data = otp_store[phone]

    if time.time() > data["expires"]:
        return False

    return data["otp"] == otp

def can_resend(phone):

    if phone in resend_store:
        if time.time() < resend_store[phone]:
            return False

    resend_store[phone] = time.time() + RESEND_TIME
    return True