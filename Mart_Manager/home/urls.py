from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name="login"),
    path('home', views.home, name='homepage'),
    path('sesh', views.getSessionInfo, name='sessions'),#Only use to print sessions in console delete after use
    path('logout', views.logout, name='logout'),
    path('blocked', views.blocking, name='blocked'),
    path('exception', views.exception, name='exception'),
    path('sessionExpired', views.sessionExpired, name='sessionExpired'),
    path('redirect-chat', views.chatRedirect, name='redirect-chat'), #redirect to mart chat
    re_path(r'^.*$', views.pageNotFound, name='404'),
]