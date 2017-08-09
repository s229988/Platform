from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.views import generic
from django.views.generic import View

from .forms import CustomerForm, LoginForm
from .models import Orders

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
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/customer/newOrders')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomerForm()

    customerID = request.user.username
    articles = Orders.objects.filter(costumer=customerID).defer("article_image")

    return render(request, 'newOrders.html', {'form': form, 'article_list': articles})

def overview(request):
    customerID = request.user.username
    articles = Orders.objects.filter(costumer=customerID).defer("article_image")
    return render(request, 'overview.html', {'article_list': articles})


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
