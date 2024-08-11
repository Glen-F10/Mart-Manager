from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name="login"),
    path('home', views.home, name='homepage'),
    path('sesh', views.getSessionInfo, name='sessions'),#Only use to print sessions in console delete after use
    path('logout', views.logout, name='logout'),
    path('Shop', views.ShopPage, name='Shop'),
    path('Shop-Manager', views.ShopManagerPage, name='Shop-Manager'),
    path('Mart-Stock', views.ShopStockPage, name='Mart-Stock'),
    path('Admin', views.AdminPage, name='Admin'),
]