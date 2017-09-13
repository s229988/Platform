from __future__ import unicode_literals
from django.db import models



class Customers(models.Model):
    companyname = models.CharField(max_length=100, blank=True, null=True)
    streetname = models.CharField(max_length=100, blank=True, null=True)
    streetnumber = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postalcode = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class Machines(models.Model):
    producer = models.ForeignKey('Producers', models.DO_NOTHING)
    capacity = models.IntegerField(blank=True, null=True)
    machinename = models.CharField(max_length=100, blank=True, null=True)

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
    customers = models.ForeignKey(Customers, models.DO_NOTHING)
    article_nr = models.IntegerField(blank=True, null=True)
    article_name = models.TextField(blank=True, null=True)
    article_file = models.TextField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    price_offer = models.FloatField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

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

    class Meta:
        managed = False
        db_table = 'producers'
