from django.forms import ModelForm
from Producer.models import Machines
from django import forms
from django.db import models

# class CapacityForm(ModelForm):
#     class Meta:
#         model = Machines
#         fields = ['id', 'producer', 'capacity']


class CapacityForm(forms.Form):
#    machine_id = forms.IntegerField(label='Maschinen-ID')
    machinename = forms.CharField(label='Name der Maschine')
    capacity = forms.IntegerField(label='Vorhandene Kapazität')
