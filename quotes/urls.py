from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path(r'', views.quote, name='index'),
    path(r'quote/', views.quote, name='get_random_quote'),
    path(r'show_all/', views.show_all, name='show_all_quotes'),
    path(r'about/', views.about, name='about'),
    
]