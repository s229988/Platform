from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connection

from .models import Orders, Machines, Matches, Producers
from .forms import CapacityForm

def redirect(request):
    return HttpResponseRedirect('/producer/assignments')

def assignments(request):
    producerID = request.user.username

    cursor = connection.cursor()
    cursor.execute("SELECT o.article_id, o.amount, o.price_offer, m.id, o.create_date, o.start_date, o.end_date, m.status FROM orders o, producers p, machines ma, matches m WHERE ma.producer_id=%s AND m.machine_id = ma.id AND m.order_id = o.id GROUP BY m.id", [producerID])
    articles = cursor.fetchall()

    context = {"article_list": articles}

    # machines = Machines.objects.filter(producer=1)
    # matches = Matches.objects.filter(machine=machines)
    # orders = Orders.objects.filter(id=matches.pk)
    #
    # context = {"article_list": orders}

    return render(request, 'assignments.html', context)


def capacity(request):
    producerID = (request.user.username)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CapacityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            machine_id = form.cleaned_data['machine_id']
            capa = form.cleaned_data['capacity']

            # create new entry in database
            producerKey = Producers.objects.get(pk=producerID)
            newCapa = Machines(producer=producerKey, capacity=capa, price=0)
            newCapa.save()



            # redirect to a new URL:
            return HttpResponseRedirect('/producer/capacity')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CapacityForm()

    capacities = Machines.objects.filter(producer=producerID).defer("price")

    return render(request, 'capacity.html', {'form': form, 'capacity_list': capacities})