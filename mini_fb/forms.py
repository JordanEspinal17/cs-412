from django import forms
from .models import Profile
from .models import StatusMessage


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']  # List the fields that will be in the form

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']  # Only the message will be input by the user

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Exclude 'first_name' and 'last_name' from the form
        fields = ['city', 'email', 'profile_image_url']

class UpdateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']

