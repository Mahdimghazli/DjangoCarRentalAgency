from django.urls import path, include, re_path
#from django.conf.urls import url
from django.contrib import admin
from . import views

from system.views import *

re_path(r'^carlist/$', car_list, name='car_list'),


urlpatterns = [
    re_path(r'^$', home, name = "home"),
    

    
    re_path(r'^carlist/$', car_list, name = "car_list"),
    re_path(r'^index_order/$', index_order, name = "index_order"),
    re_path(r'^contact/$', msg, name = "msg"),



    re_path(r'^(?P<car_id>\d+)/createOrder/$', order_created, name="order_create"),

    re_path(r'^(?P<id>\d+)/edit/$', car_update, name = "car_edit"),


    re_path(r'^(?P<id>\d+)/$', car_detail, name = "car_detail"),
    re_path(r'^detail/(?P<id>\d+)/$', order_detail, name = "order_detail"),

    re_path(r'^(?P<id>\d+)/delete/$', car_delete, name = "car_delete"),
    re_path(r'^(?P<id>\d+)/deleteOrder/$', order_delete, name = "order_delete"),

    re_path(r'^contact/$', contact, name = "contact"),

    re_path(r'^newcar/$', newcar, name = "newcar"),
    re_path(r'^(?P<id>\d+)/like/$', like_update, name = "like"),
    re_path(r'^popularcar/$', popular_car, name = "popularcar"),

]
