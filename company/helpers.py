from .models import *
from django.conf import settings
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response

def authenticate(self, request, company_email=None, password=None):
        
        try :
            user = Companies.objects.get(company_email=company_email)
            name=user.company_email
            v_pass=user.password
            login_valid = (name == company_email)
            pwd_valid = check_password(password,v_pass)
        except:
            login_valid = (None == company_email)
        if login_valid and pwd_valid:
            try:
                user = Companies.objects.get(company_email=company_email)
            except Companies.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = Companies(company_email=company_email)
                user.save()
            return user
        return None


def authenticateMyUser(self, request, email=None, password=None):
        
        try :
            user = Users.objects.get(email=email)
            email=user.email
            v_pass=user.password
            login_valid = (email == email)
            pwd_valid = check_password(password,v_pass)
        except:
            login_valid = (None == email)
        if login_valid and pwd_valid:
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                user = Users(email=email)
                user.save()
            return user
        return None