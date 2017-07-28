from django import forms

class CustomerForm(forms.Form):
    product_ID = forms.CharField(label='Bitte Artikel-ID eingeben ', max_length=100)