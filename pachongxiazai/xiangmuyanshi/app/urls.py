from django.urls import path
from . import views


urlpatterns = [
    path('xm', views.xm, name='xm'),
    path('LT', views.LT, name='LT'),





]