from django.views.generic import ListView, DetailView,CreateView
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect


class ShowAllProfilesView(ListView):
    model = Profile  # This fetches all profiles from the database
    template_name = 'mini_fb/show_all_profiles.html'  # Template for the view
    context_object_name = 'profiles'  # Context name for the list of profiles

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
    # Redirect back to the profile page using the profile's pk from the URL kwargs
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

    
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        # Associate the status message with the correct profile
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile

        # Save the form and set self.object
        response = super().form_valid(form)

        # Handle the uploaded files
        files = self.request.FILES.getlist('files')
        for f in files:
            img = Image(image_file=f, status_message=self.object)
            img.save()

        return response

    def get_success_url(self):
        # Use self.object.profile.pk or self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the profile to the template context
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
