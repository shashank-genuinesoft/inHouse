import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from . models import *
def send_otp(company_id,email):
        otp = random.randint(999,9999)
        key=Companies.objects.get(company_id=company_id)
        key.code=otp
        key.save()
        subject, from_email, to = 'Verify account', 'shashankpathe@gmail.com', email
        text_content = 'This is an important message.'
        context={ "otp":otp,}
        html_content =  render_to_string('otp.html',context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content,"text/html")
        msg.send()