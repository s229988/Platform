from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', login, {'template_name': 'login_producer.html'}, name='login_producer'),
    url(r'^login/$', login, {'template_name': 'login_producer.html'}, name='login_producer'),
    url(r'^assignments/$', views.assignments, name='assignments'),
    url(r'^add_machine/$', views.add_machine, name='add_machine'),
    url(r'^login/redirect/$', views.redirect, name='redirect'),
    url(r'^assignments/(?P<item_id>[0-9]+)/(?P<new_status>[0-9]+)/$', views.safe_status, name="safe_status"),
    url(r'^add_machine/(?P<machine_id>[0-9]+)/$', views.change_capacity, name="change_capacity"),
    url(r'^add_machine/delete/(?P<machine_id>[0-9]+)/$', views.delete_machine, name="delete_machine"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^logout/redirect/$', views.redirectStartpage, name='redirectStartpage'),
]