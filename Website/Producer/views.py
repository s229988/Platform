from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connection
from django.shortcuts import render_to_response
from django.contrib import messages

from .models import Orders, Machines, Matches, Producers
from .forms import CapacityForm

def redirect(request):
    return HttpResponseRedirect('/producer/assignments')

def assignments(request):
    producerID = request.user.username

    cursor = connection.cursor()
    cursor.execute("SELECT o.article_id, o.amount, o.price_offer, o.create_date, o.start_date, o.end_date, o.status FROM orders o WHERE o.status = 'pending'")
    articles_pending = cursor.fetchall()

    cursor.execute("SELECT o.article_id, o.amount, o.price_offer, ma.id, o.create_date, o.start_date, o.end_date, o.status, o.id FROM orders o, producers p, machines ma, matches m WHERE ma.producer_id=%s AND m.machine_id = ma.id AND m.order_id = o.id AND o.status = 'in production' GROUP BY m.id", [producerID])
    articles_inproduction = cursor.fetchall()

    cursor.execute("SELECT o.article_id, o.amount, o.price_offer, ma.id, o.create_date, o.start_date, o.end_date, o.status FROM orders o, producers p, machines ma, matches m WHERE ma.producer_id=%s AND m.machine_id = ma.id AND m.order_id = o.id AND o.status = 'done' GROUP BY m.id", [producerID])
    articles_done = cursor.fetchall()

    context = {"articles_pending": articles_pending, "articles_inproduction": articles_inproduction,  "articles_done": articles_done }

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

            # machine_id = form.cleaned_data['machine_id']
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


def change_status(request, item_id, new_status):
    if new_status == '1':
        status_changed = Orders.objects.filter(pk=item_id).update(status='pending')
    if new_status == '2':
        status_changed = Orders.objects.filter(pk=item_id).update(status='done')

    return HttpResponseRedirect('/producer/assignments')


def change_capacity(request, machine_id):
    if request.method == 'POST':
        new_capa = request.POST.get('new_capacity')
        # set new value 'new_capacity' to the object
        new_capacity = Machines.objects.filter(pk=machine_id).update(capacity=new_capa)
        return HttpResponseRedirect('/producer/capacity')

def delete_machine(request, machine_id):
    # matches = Matches.objects.only('machine')

    cursor = connection.cursor()
    cursor.execute("SELECT machine_id FROM website.matches")
    matches = cursor.fetchall()

    if machine_id in matches:
        messages.add_message(request, messages.INFO, 'Test')
    else:
      machine_deleted = Machines.objects.filter(pk=machine_id).delete()

    return HttpResponseRedirect('/producer/capacity')

