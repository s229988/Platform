from django.contrib import admin
from django.http import HttpResponseRedirect

import subprocess
from django.contrib.admin.views.decorators import staff_member_required

def matching(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # call matching script
        subprocess.call(["python", "C:/Users/s229988/PycharmProjects/Platform/MatchingProgramm/matching.py"])
        # send mail
        subprocess.call(["python", "C:/Users/s229988/PycharmProjects/Platform/MatchingProgramm/sendmail.py"])

        # redirect to a new URL:
        return HttpResponseRedirect('/admin/')

    # if a GET (or any other method) we'll create a blank form

    return HttpResponseRedirect('/admin/')
