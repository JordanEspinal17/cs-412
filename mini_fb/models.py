from django.db import models
from django.utils import timezone

class Profile(models.Model):
    # Existing fields...
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image_url = models.URLField()

    # Existing methods...
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')

class StatusMessage(models.Model):
    # Existing fields...
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # Existing methods...
    def __str__(self):
        return f"{self.profile.first_name}: {self.message[:30]}..."

    def get_images(self):
        return self.image_set.all()

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for StatusMessage {self.status_message.id} at {self.timestamp}"
