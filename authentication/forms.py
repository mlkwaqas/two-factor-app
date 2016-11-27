from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from authentication.models import UserProfile


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password')
    country_code = forms.IntegerField(label='Country code')
    phone_number = forms.CharField(label='Phone number', max_length=100)

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("User is already registered with this email")

        return data

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        country_code = self.cleaned_data['country_code']
        if UserProfile.objects.filter(phone_number=phone_number, country_code=country_code).exists():
            raise forms.ValidationError("User is already registered with this phone number")

        return phone_number


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password')


class VerifyForm(forms.Form):
    token = forms.CharField(label='Token')
