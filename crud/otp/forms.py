from django import forms
from django.utils.translation import gettext as _
from otp.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from collections import OrderedDict

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'userType', 'userRole', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            email = email.lower()
            User._default_manager.get(email=email)
            raise forms.ValidationError("Email already Exists")
        except:
            return email

    def clean_password2(self):
        self.error_messages = {"password_mismatch": _("Password Do Not Match"),
                               }
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        if len(password1) < int(8):
            raise forms.ValidationError("This Password is to sort")
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.userType = self.cleaned_data['userType']
        user.userRole = self.cleaned_data['userRole']
        user.set_password(self.cleaned_data['password2'])

        if commit:
            user.save()

        return user

from .models import firstOTP

class generateOTPForm(ModelForm):
    class Meta:
        model = firstOTP
        fields = ['email', 'otp', 'is_verified']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            email = email.lower()
            a = firstOTP.get(email=email)
            print("aaa", a)
            raise forms.ValidationError("Email already Exists")
        except:
            return email