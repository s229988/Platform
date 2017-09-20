from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect



def startpage(request):
    return render(request, 'startpage.html')
