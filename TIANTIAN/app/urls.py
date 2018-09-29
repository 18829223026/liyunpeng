from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('list/', views.goods_list, name='list'),
    path('detail/', views.detail, name='detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('order/', views.order, name='order'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('center_info/', views.center_info, name='center_info'),
    path('center_order/', views.center_order, name='center_order'),
    path('center_site/', views.center_site, name='center_site'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),


]