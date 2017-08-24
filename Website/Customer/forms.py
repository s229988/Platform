from django import forms
from django.contrib.auth.models import User

class CustomerForm(forms.Form):
   product_ID = forms.CharField(label='Bitte Produktions-ID eingeben ')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']