from django.contrib import admin
from .models import UploadedVideo, Profile, CoachFeedback, Achievement
from .models import Ranking


# Register your models here
admin.site.register(UploadedVideo)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'videos_uploaded')
    search_fields = ('user__username',)
    list_filter = ('videos_uploaded',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'condition')
    search_fields = ('name', 'condition')
@admin.register(CoachFeedback)
class CoachFeedbackAdmin(admin.ModelAdmin):
    list_display = ('video', 'created_at')
    search_fields = ('feedback_text',)
@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('username', 'score', 'video')