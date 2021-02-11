import os
from django.shortcuts import render
from django.http import HttpResponse
from http.client import responses
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from twilio.rest import Client
from django.views.generic import TemplateView
from random import randint
from .models import PhoneOTP

def sendotp(phone):
      OTPcode = randint(10000, 99999) 
      phonenumber = phone
      account_sid = 'YOUR Twilio SID'
      auth_token =  'Your Twilio Token'
      client = Client(account_sid, auth_token)
      message = client.messages.create(
          from_='Twilio Virtual Phone number',
          body= 'Your OTP password is '+str(OTPcode),
          to='+91'+phonenumber
          )
      return OTPcode

def OTPview(request):
    phone = request.session['phone_number']
    return render(request, 'otp.html', {'phone':phone})

def post(request):
    if request.method == "POST":
        phone_number = request.POST['phone']
        request.session['phone_number'] = phone_number
        if phone_number:
            phone  = str(phone_number)
            user = PhoneOTP.objects.filter(phone__iexact = phone)

            if user.exists():
                return render(request,'register.html',{
                   'detail': 'Phone number already registered.'
                    })
            else:
                OTPcode = sendotp(phone)
                new = PhoneOTP.objects.create(
                            phone = phone,
                            otp = OTPcode,
                            )
                return redirect('otp')
    return render(request,'register.html')

def ValidOTP(request):
       if request.method == "POST":
        phone = request.session['phone_number']
     
        otp_sent = request.POST['notp']
        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                count = old.count
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.otp = ""
                    old.count = count + 1 
                    old.save()
                    return redirect('success')
                else:
                   return render(request,'otp.html',{
                     'detail': 'OTP incorrect'
                      })    
            else:
                   return render(request,'otp.html',{
                     'detail': 'OTP incorrect'
                      })            
        else:
          return render(request,'otp.html',{
            'detail': 'OTP incorrect & empty'
            })      

def send_otp(phone):
    if phone:
        key = randint(10000, 99999)
        print(key)
        return key
    else:
        return False