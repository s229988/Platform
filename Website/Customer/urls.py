from django.conf.urls import url
from . import views, admin
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^newOrders/$', views.newOrders, name='newOrders'),
    url(r'^login/redirect/$', views.redirect, name='redirect'),
    url(r'^matching/$', admin.matching, name='redirect'),
    url(r'^newOrders/(?P<item_id>[0-9]+)/$', views.delete_item, name="delete_item"),
]
