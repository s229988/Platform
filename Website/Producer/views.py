from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connection
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import subprocess

from .models import Orders, Machines, Matches, Producers
from .forms import CapacityForm

def redirect(request):
    return HttpResponseRedirect('/producer/assignments')

def redirectStartpage(request):
    return HttpResponseRedirect('/producer/login')


@login_required
def assignments(request):
    producerID = request.user.username

    subprocess.check_output(['python', 'C:/Users/s229988/PycharmProjects/Platform/Matching/checkmail.py'])


    cursor = connection.cursor()

    cursor.execute("SELECT  o.production_nr, o.article_nr, o.article_name, o.amount, o.price_offer, c.companyname, o.create_date, o.start_date, o.end_date, o.status FROM orders o, customers c WHERE o.status = 'pending' AND c.id = o.customer_id")
    articles_pending = cursor.fetchall()

    cursor.execute("SELECT  o.production_nr, o.article_nr, o.article_name, o.amount, o.price_offer, c.companyname, ma.machinename, o.create_date, o.start_date, o.end_date, o.status, o.id FROM orders o, producers p, machines ma, matches m, customers c WHERE ma.producer_id=%s AND m.machine_id = ma.id AND m.order_id = o.id AND o.status = 'in production' AND c.id = o.customer_id GROUP BY m.id", [producerID])
    articles_inproduction = cursor.fetchall()

    cursor.execute("SELECT  o.production_nr, o.article_nr, o.article_name, o.amount, o.price_offer, c.companyname, ma.machinename, o.create_date, o.start_date, o.end_date, o.status FROM orders o, producers p, machines ma, matches m, customers c WHERE ma.producer_id=%s AND m.machine_id = ma.id AND m.order_id = o.id AND o.status = 'done' AND c.id = o.customer_id GROUP BY m.id", [producerID])
    articles_done = cursor.fetchall()

    context = {"articles_pending": articles_pending, "articles_inproduction": articles_inproduction,  "articles_done": articles_done }

    return render(request, 'assignments.html', context)


@login_required
def add_machine(request):
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
            name = form.cleaned_data['machinename']

            machinenames = Machines.objects.only('machinename')

            if capa >= 0:
                if Machines.objects.filter(machinename=name).exists():
                    messages.add_message(request, messages.ERROR, 'Machine name already used. Please choose another name.')
                else:
                    # create new entry in database
                    producerKey = Producers.objects.get(pk=producerID)
                    newCapa = Machines(producer=producerKey, capacity=capa, machinename=name)
                    newCapa.save()
            else:
                messages.add_message(request, messages.ERROR,'The Capacity is not allowed to be negative. Please enter a valid value.')

            # redirect to a new URL:
            return HttpResponseRedirect('/producer/add_machine')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CapacityForm()

    capacities = Machines.objects.filter(producer=producerID)

    return render(request, 'capacity.html', {'form': form, 'capacity_list': capacities})


@login_required
def safe_status(request, item_id, new_status):
    if new_status == '1':
        status_changed = Orders.objects.filter(pk=item_id).update(status='pending')
    if new_status == '2':
        status_changed = Orders.objects.filter(pk=item_id).update(status='done')

    return HttpResponseRedirect('/producer/assignments')


@login_required
def change_capacity(request, machine_id):
    if request.method == 'POST':
        new_capa = int(request.POST.get('new_capacity'))

        # set new value 'new_capacity' to the object
        if new_capa >= 0:
            # create new entry in database
            new_capacity = Machines.objects.filter(pk=machine_id).update(capacity=new_capa)
        else:
            messages.add_message(request, messages.ERROR, 'The Capacity is not allowed to be negative. Please enter a valid value.')

    return HttpResponseRedirect('/producer/add_machine')


@login_required
def delete_machine(request, machine_id):
    cursor = connection.cursor()
    query = 'SELECT COUNT(machine_id) FROM website.matches WHERE machine_id="{}"'.format(machine_id)
    cursor.execute(query)
    matches = cursor.fetchall()

    if matches[0][0] > 0:
        messages.add_message(request, messages.ERROR, 'The chosen machine can´t be deleted, because there are ongoing orders matched to this machine.')
    else:
        machine_deleted = Machines.objects.filter(pk=machine_id).delete()

    return HttpResponseRedirect('/producer/add_machine')
