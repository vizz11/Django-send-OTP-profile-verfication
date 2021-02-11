from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.

class PhoneOTP(models.Model):
     email = models.EmailField(max_length=254, unique=True, blank=True, default=False)
     phone_regex = RegexValidator(regex = r'^[6-9]\d{9}$', message = "Phone number must be entered in the form of +919999999999.")
     name = models.CharField(max_length=254, blank=True, null=True)
     phone = models.CharField(validators =[phone_regex], max_length=17)
     otp = models.CharField(max_length=9, blank=True, null=True,unique=True,)
     count = models.IntegerField(default=0, help_text = 'Number of opt_sent')
     validated = models.BooleanField(default=False, help_text= 'if it is true, that means user have validate opt correctly in seconds')

     def __str__(self):
         return str(self.phone)