from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import UserRegisterView, profile_page
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.base, name='webcam/base'),
    path('upload_video', views.upload_video, name='upload_video'),
    path('analyze/<int:video_id>/', views.analyze_video, name='analyze_video'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='webcam/login.html'), name='login'),
    path('logout_success/', views.logout_success, name='logout_success'),
    path('leaderboard/', views.global_leaderboard, name='global_leaderboard'),
    path('dance_routine/', views.generate_dance_routine, name='dance_routine'),
    path('profile/', profile_page, name='profile_page'),
    path('message/update/<int:message_id>/', views.update_message, name='update_message'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('reset_all_scores/', views.reset_all_scores, name='reset_all_scores'),
    path('delete_all_scores/', views.delete_all_scores, name='delete_all_scores'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
