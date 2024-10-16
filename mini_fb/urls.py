from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),  # All profiles
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),  # Single profile
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),  # Status message creation
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),  # Profile creation
]
