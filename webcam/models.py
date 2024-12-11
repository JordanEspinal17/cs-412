from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django import forms



class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='webcam_profile'  # Unique related_name
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    videos_uploaded = models.IntegerField(default=0)  # Track the number of videos uploaded
    achievements = models.ManyToManyField('Achievement', blank=True)

    def __str__(self):
        return self.user.username


class UploadedVideo(models.Model):
    client_video = models.FileField(upload_to='uploaded_videos/')
    reference_video = models.FileField(upload_to='reference_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    client_duration = models.FloatField(null=True, blank=True)
    reference_duration = models.FloatField(null=True, blank=True)


class CoachFeedback(models.Model):
    video = models.ForeignKey(UploadedVideo, on_delete=models.CASCADE, related_name="feedbacks")
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Video {self.video.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Ranking(models.Model):
    username = models.CharField(max_length=150)
    score = models.FloatField()
    video = models.ForeignKey('UploadedVideo', on_delete=models.CASCADE, related_name='rankings')

    def __str__(self):
        return f"{self.username} - {self.score}"

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge = models.ImageField(upload_to='badges/')  # Optional: Badge image for visual representation
    condition = models.CharField(max_length=100)  # Condition (e.g., "uploaded_5_videos")

    def __str__(self):
        return self.name
    
