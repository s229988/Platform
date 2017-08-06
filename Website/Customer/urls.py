from django.conf.urls import url
from . import views
from django.contrib.auth.views import login


urlpatterns = [
    url(r'^$', views.newOrders, name='newOrders'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^overview', views.overview, name='overview'),
    url(r'^newOrders', views.newOrders, name='newOrders'),
]
