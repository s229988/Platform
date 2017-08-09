from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', login, {'template_name': 'login_producer.html'}, name='login_producer'),
    url(r'^login/$', login, {'template_name': 'login_producer.html'}, name='login_producer'),
    url(r'^assignments', views.assignments, name='assignments'),
    url(r'^capacity', views.capacity, name='capacity'),
    url(r'^login/redirect/', views.redirect, name='redirect'),
]