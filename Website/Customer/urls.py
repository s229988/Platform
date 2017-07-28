from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.newOrders, name='newOrders'),
    url(r'^overview', views.overview, name='overview'),
    url(r'^newOrders', views.newOrders, name='newOrders'),
]
