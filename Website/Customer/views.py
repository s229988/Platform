from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.views import generic
from django.views.generic import View

from .forms import CustomerForm, LoginForm
from .models import Orders

import subprocess


def redirect(request):
    return HttpResponseRedirect('/customer/overview')

def newOrders(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            formdata = form.cleaned_data['product_ID']
            # process the data in form.cleaned_data as required

            subprocess.call(['python', 'C:/Users/s229988/PycharmProjects/Platform/ERPProgramm/crawl.py', formdata])

            # redirect to a new URL:
            return HttpResponseRedirect('/customer/newOrders')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomerForm()

    customerID = request.user.username
    articles_pending = Orders.objects.filter(customer=customerID, status="pending").defer("article_image")

    return render(request, 'newOrders.html', {'form': form, 'articles_pending': articles_pending})

def overview(request):
    customerID = request.user.username
    articles_pending = Orders.objects.filter(customer=customerID, status="pending").defer("article_image")
    articles_inproduction = Orders.objects.filter(customer=customerID, status="in production").defer("article_image")
    articles_notmatched = Orders.objects.filter(customer=customerID, status="not matched").defer("article_image")
    articles_done = Orders.objects.filter(customer=customerID, status="done").defer("article_image")

    return render(request, 'overview.html', {'articles_pending': articles_pending, 'articles_inproduction': articles_inproduction, 'articles_notmatched': articles_notmatched, 'articles_done': articles_done})




def delete_item(request, item_id):
    customerID = request.user.username
    articles_deleted = Orders.objects.filter(customer=customerID, pk=item_id).delete()
    return HttpResponseRedirect('/customer/newOrders')


# class LoginFormView(View):
#     form_class = LoginForm
#     template_name = 'login.html'
#
#     # display blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     # process form data
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
# #            user = form.save(commit=False)
#
#             # clean data
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
# #            user.set_password(password)
# #            user.save()
#
#             # return User objects if credentials are correct
#             user = auth.authenticate(username=username, password=password)
#
#             if user is not None:
#                 if user.is_active:
#
#                     auth.login(request, user)
#                     return redirect('/customer/overview/')
#
#         return render(request, self.template_name, {'form': form})
