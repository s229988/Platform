from django import forms
from django.contrib.auth.models import User

class CustomerForm(forms.Form):
   product_ID = forms.CharField(label='Bitte Produktions-ID eingeben ')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

#https://stackoverflow.com/questions/31291611/restricting-user-access-to-different-apps-in-django