from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.quote, name='index'),
    path('quote/', views.quote, name='get_random_quote'),
    path('show_all/', views.show_all, name='show_all_quotes'),
    path('about/', views.about, name='about'),
    
]