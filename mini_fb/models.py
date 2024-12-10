from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User  # Import User model



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image_url = models.URLField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username if self.user else 'No User'})"


    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')
    
    def get_friends(self):
        friendships = Friend.objects.filter(
            Q(profile1=self) | Q(profile2=self)
        )
        friends = [friendship.profile2 if friendship.profile1 == self else friendship.profile1 for friendship in friendships]
        return friends

    def add_friend(self, other):
        # Check if 'self' is the same as 'other'
        if self == other:
            return  # Do nothing if trying to friend oneself

        # Check if the friendship already exists
        if not Friend.objects.filter(
            (Q(profile1=self) & Q(profile2=other)) | 
            (Q(profile1=other) & Q(profile2=self))
        ).exists():
            # Create the friendship if it doesn't exist
            Friend.objects.create(profile1=self, profile2=other)

    def get_news_feed(self):
        # Get the list of this profile's friends
        friends = self.get_friends()

        # Get status messages for this profile and all friends
        profiles_to_include = [self] + friends
        news_feed = StatusMessage.objects.filter(profile__in=profiles_to_include).order_by('-timestamp')
        return news_feed

    def get_friend_suggestions(self):
        # Get all profiles except self and current friends
        friends = self.get_friends()
        friend_ids = [friend.id for friend in friends]
        return Profile.objects.exclude(id__in=friend_ids + [self.id])

class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name='friend_profile1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name='friend_profile2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"


class StatusMessage(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Existing field

    def __str__(self):
        return f"{self.profile.first_name}: {self.message[:30]}..."

    def get_images(self):
        return self.images.all()  # Updated to use 'images' related_name



class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(
        StatusMessage,
        on_delete=models.CASCADE,
        related_name='images'  # Add this line
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for StatusMessage {self.status_message.id} at {self.timestamp}"
