from django.db import models
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image_url = models.URLField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')  # Return status messages ordered by most recent

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})  # Return the URL to show this profile


class StatusMessage(models.Model):
    message = models.TextField()  # Stores the text of the status message
    timestamp = models.DateTimeField(default=timezone.now)  # Automatically set the time when the status is created
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Link to the Profile model

    def __str__(self):
        return f"{self.profile.first_name}: {self.message[:30]}..."  # Display the first 30 chars of the message
