from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader

from .forms import CustomerForm
from .models import Orders

def newOrders(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/customer/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomerForm()

    return render(request, 'newOrders.html', {'form': form})

def overview(request):
    i = 0
    article_Set = Orders.Objects.all()
    for articles in article_Set:
        article_Name[i] = article_Set.article_id
        i = i+1
    return render(request, 'overview.html', {'article': article_Name[0]})

