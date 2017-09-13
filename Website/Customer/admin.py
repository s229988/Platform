from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import Machines, Orders
from django.contrib import messages

import subprocess
from django.contrib.admin.views.decorators import staff_member_required

def matching(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # call matching script
        if Machines.objects.all().exists():
            if Orders.objects.filter(status= 'pending').exists():
                subprocess.call(["python", "C:/Users/s229988/PycharmProjects/Platform/MatchingProgramm/matching.py"])
                # send mail
                subprocess.call(["python", "C:/Users/s229988/PycharmProjects/Platform/MatchingProgramm/sendmail.py"])

                messages.add_message(request, messages.ERROR, 'Matching successfully completed.')

                # redirect to a new URL:
                return HttpResponseRedirect('/admin/')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Matching can not be started. Please check if there are pending orders.')

        else:
            messages.add_message(request, messages.ERROR, 'Matching can not be started. Please ensure that machines are maintained.')

    # if a GET (or any other method) we'll create a blank form

    return HttpResponseRedirect('/admin/')
