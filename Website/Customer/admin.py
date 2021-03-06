from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import Machines, Orders, Customers
from django.contrib import messages

import subprocess

def matching(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # call matching script
        if Machines.objects.all().exists():
            if Orders.objects.filter(status= 'pending').exists():
                subprocess.call(["python", "C:/Users/s229988/PycharmProjects/Platform/Matching/matching.py"])
                # send mail
                subprocess.call(["python", "C:/Users/s229988/PycharmProjects/Platform/Matching/sendmail.py"])

                messages.add_message(request, messages.ERROR, 'Matching successfully completed. Emails have been send to all producers to inform them what to produce.')

                # redirect to a new URL:
                return HttpResponseRedirect('/admin/')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Matching can not be started. Please check if there are pending orders.')

        else:
            messages.add_message(request, messages.ERROR, 'Matching can not be started. Please ensure that machines are maintained.')

    # if a GET (or any other method) we'll create a blank form

    return HttpResponseRedirect('/admin/')
