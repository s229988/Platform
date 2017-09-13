from django.forms import ModelForm
from Producer.models import Machines
from django import forms
from django.db import models

# class CapacityForm(ModelForm):
#     class Meta:
#         model = Machines
#         fields = ['id', 'producer', 'capacity']


class CapacityForm(forms.Form):
    machinename = forms.CharField(label='Machine name ')
    capacity = forms.IntegerField(label='Available Capacity')
