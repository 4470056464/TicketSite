from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from . import views
# app_name='accounts'

urlpatterns = [
    url('login', views.login, name='login'),
    url('logout', views.logout, name='logout'),
    url('register', views.register, name='register'),
    url('dashboard', views.dashboard, name='dashboard'),
    url('phoneLogin/',views.PhoneLogin,name='PhoneLogin'),
    path('verifycode/<int:phone>/<int:randNum>/',views.verify_code,name='verifyCode'),

]
