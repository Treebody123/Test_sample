#encoding: utf-8

from django.urls import path
from . import views

app_name = 'xfzauth'

urlpatterns = [
    path("login/",views.LoginView.as_view(),name='login'),
    path("register/",views.RegisterView.as_view(),name='register'),
    path("img_captcha/",views.img_captcha,name='img_captcha'),
    path("sms_captcha/",views.sms_captcha,name='sms_captcha'),
    path("logout/",views.logout_view,name='logout'),
]