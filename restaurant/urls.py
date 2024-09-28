from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path(r'', views.main, name='index'),
    path(r'main/', views.main, name='main'),
    path(r'order/', views.order, name='order'),
    path(r'confirmation/', views.confirmation , name='confirmation'),
]