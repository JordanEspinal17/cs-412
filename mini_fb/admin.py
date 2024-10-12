from django.contrib import admin
from .models import Profile, StatusMessage

# Register both Profile and StatusMessage models
admin.site.register(Profile)
admin.site.register(StatusMessage)
