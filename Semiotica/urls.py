"""Semiotica URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from copy_cat import views

urlpatterns = [
    url(r'^$', views.home, name='root'),
    url(r'^home/', views.home, name='home'),
    url(r'^index/', views.index, name='index'),
	url(r'^chat/', include('copy_cat.urls')),
    url(r'^analysis/', views.analysis, name='analysis'),
    url(r'^walkAB/$', views.walk_home, name='walk_home'),
    url(r'^walkAB/result/(?P<r>[0-9]+)/', views.walk_result, name='walk_result'),
    url(r'^admin/', admin.site.urls)]