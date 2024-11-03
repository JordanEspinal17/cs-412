from django.urls import path
from .views import (
    ShowAllProfilesView, ShowProfilePageView, CreateProfileView,
    CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView,
    UpdateStatusMessageView, CreateFriendView, ShowFriendSuggestionsView,
    ShowNewsFeedView, UserRegisterView
)
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mini_fb'


urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),  # All profiles
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),  # Single profile
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),  # Profile creation
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/<int:pk>/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logout.html'), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)