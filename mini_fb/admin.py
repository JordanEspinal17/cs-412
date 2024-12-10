from django.contrib import admin
from .models import Profile, Friend, StatusMessage, Image

admin.site.register(Profile)
admin.site.register(Friend)
admin.site.register(StatusMessage)
admin.site.register(Image)
