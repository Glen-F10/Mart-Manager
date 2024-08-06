from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('home', views.home, name='homepage'),
    path('sesh', views.getSessionInfo, name='sessions'),#Only use to print sessions in console delete after use
]