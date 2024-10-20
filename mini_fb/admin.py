from django.contrib import admin
from .models import Profile, StatusMessage, Image  # Import Image model

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)  # Register Image model
