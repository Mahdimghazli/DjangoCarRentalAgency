"""car_rental_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from system.views import admin_car_list, admin_msg, order_list, car_created, order_update, order_delete, msg_delete
from accounts.views import (login_view, register_view, logout_view)
from django.urls import path
from myapp.views import register, user_login, user_logout

urlpatterns = [
    #re_path(r'^$', admin_car_list, name='adminIndex'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),



    #vers system
    re_path(r'^', include('system.urls')),

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^listOrder/$', order_list, name = "order_list"),
    re_path(r'^(?P<id>\d+)/editOrder/$', order_update, name = "order_edit"),
    re_path(r'^(?P<id>\d+)/deleteOrder/$', order_delete, name = "order_delete"),
    re_path(r'^create/$', car_created, name = "car_create"),
    re_path(r'^message/$', admin_msg, name='message'),
    re_path(r'^(?P<id>\d+)/deletemsg/$', msg_delete, name = "msg_delete"),    
   # re_path(r'^login/', login_view, name='login'),
    #re_path(r'^logout/', logout_view, name='logout'),
  #  re_path(r'^register/', register_view, name='register'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)