"""loginProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from mainapp import views

urlpatterns = [
    path('', views.home),
    path('login', views.login),
    path('regist', views.regist),
    path('home_logined', views.home_logined),
    path('userinfo_mod', views.userinfo_mod),
    path('logout', views.logout),
    path('upload', views.upload),
    path('list/<int:page_num>', views.list),
    path('add', views.add),

]
