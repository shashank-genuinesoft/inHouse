import pyotp
from django.conf import settings
from django.middleware import csrf

def generateKey():
    secret = pyotp.random_base32()        
    totp = pyotp.TOTP(secret, interval=86400)
    OTP = totp.now()
    return {"totp":secret,"OTP":OTP}

def verify_otp(activation_key,otp):
    totp = pyotp.TOTP(activation_key, interval=86400)
    verify = totp.verify(otp)
    return verify
