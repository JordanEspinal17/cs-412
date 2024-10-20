from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView,UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),  # All profiles
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),  # Single profile
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),  # Profile creation
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),


]
