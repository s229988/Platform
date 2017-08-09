from __future__ import unicode_literals
from django.db import models



class Costumers(models.Model):
    companyname = models.CharField(max_length=100, blank=True, null=True)
    streetname = models.CharField(max_length=100, blank=True, null=True)
    streetnumber = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postalcode = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'costumers'


class Machines(models.Model):
    producer = models.ForeignKey('Producers', models.DO_NOTHING)
    capacity = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'machines'


class Matches(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    machine = models.ForeignKey(Machines, models.DO_NOTHING)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matches'


class Orders(models.Model):
    costumer = models.ForeignKey(Costumers, models.DO_NOTHING)
    article_id = models.IntegerField(blank=True, null=True)
    article_image = models.TextField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    price_offer = models.FloatField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Producers(models.Model):
    companyname = models.CharField(max_length=100, blank=True, null=True)
    streetname = models.CharField(max_length=100, blank=True, null=True)
    streetnumber = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postalcode = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    number_machines = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producers'
