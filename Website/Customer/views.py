from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.views import generic
from django.views.generic import View
from django.contrib import messages

from .forms import LoginForm
from .models import Orders

import subprocess


def redirect(request):
    return HttpResponseRedirect('/customer/overview')

def newOrders(request):
    customerID = request.user.username
    pnr = request.POST.get('dropdown')

        # if this is a POST request we need to process the form data


    if request.method == 'POST':
        try:
            subprocess.check_output(
                ['python', 'C:/Users/s229988/PycharmProjects/Platform/ERPProgramm/crawl.py', pnr, customerID])
        except Exception:
            messages.add_message(request, messages.ERROR,
                                 'The production number {} has no Price or Article File found in your ERP System . Please check with your system'.format(
                                     pnr))
            # redirect to a new URL:
        return HttpResponseRedirect('/customer/newOrders')
        # get production numbers from ERP
    production_numbers = subprocess.check_output(['python', 'C:/Users/s229988/PycharmProjects/Platform/ERPProgramm/crawl_prodnr.py', customerID])

    # decode production_numbers
    production_numbers = production_numbers.decode("utf-8")
    production_numbers = production_numbers.replace(',', '')
    production_numbers = production_numbers.replace('[', '')
    production_numbers = production_numbers.replace(']', '')
    production_numbers = production_numbers.replace("'", '')
    production_numbers = production_numbers.split(' ')

    # parse string to int for each value in production_numbers
    i = 0
    for item in production_numbers:
        production_numbers[i] = int(item)
        i += 1

    # get all orders with status = pending
    articles_pending = Orders.objects.filter(customer=customerID, status="pending").defer("article_file")

    return render(request, 'newOrders.html', {'articles_pending': articles_pending, 'production_numbers': production_numbers})

def overview(request):
    customerID = request.user.username

    subprocess.check_output(['python', 'C:/Users/s229988/PycharmProjects/Platform/MatchingProgramm/checkmail.py'])


    articles_pending = Orders.objects.filter(customer=customerID, status="pending").defer("article_file")
    articles_inproduction = Orders.objects.filter(customer=customerID, status="in production").defer("article_file")
    articles_nomatch = Orders.objects.filter(customer=customerID, status="no match").defer("article_file")
    articles_done = Orders.objects.filter(customer=customerID, status="done").defer("article_file")

    return render(request, 'overview.html', {'articles_pending': articles_pending, 'articles_inproduction': articles_inproduction, 'articles_nomatch': articles_nomatch, 'articles_done': articles_done})


def delete_item(request, item_id):
    articles_deleted = Orders.objects.filter(pk=item_id).delete()
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
