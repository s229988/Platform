from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connection

from .models import Orders, Machines, Matches, Producers

# Create your views here.

def redirect(request):
    return HttpResponseRedirect('/producer/assignments')

def assignments(request):
    producerID = request.user.username
#    articles = Orders.objects.filter(customer=producerID).defer("article_image")

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT o.article_id, o.amount, o.price_offer, m.id, o.create_date, o.start_date, o.end_date, m.status FROM orders o, producers p, machines ma, matches m WHERE ma.producer_id=1 AND m.machine_id = ma.id AND m.order_id = o.id")
    #     articles = cursor.fetchall()
    #
    # context = {"article_list": articles}

    cursor = connection.cursor()
    cursor.execute("SELECT o.article_id, o.amount, o.price_offer, m.id, o.create_date, o.start_date, o.end_date, m.status FROM orders o, producers p, machines ma, matches m WHERE ma.producer_id='1' AND m.machine_id = ma.id AND m.order_id = o.id GROUP BY m.id")
    articles = cursor.fetchall()

    context = {"article_list": articles}


    # machines = Machines.objects.filter(producer=1)
    # matches = Matches.objects.filter(machine=machines)
    # orders = Orders.objects.filter(id=matches.pk)
    #
    # context = {"article_list": orders}


    return render(request, 'assignments.html', context)


def capacity(request):
    return HttpResponse("Kapazität")