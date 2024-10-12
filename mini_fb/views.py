from django.views.generic import ListView, DetailView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse
from django.views.generic.edit import CreateView

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
        return reverse('show_profile', kwargs={'pk': self.object.pk})  # After creating, redirect to the profile page
    
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])  # Get the Profile based on the pk in the URL
        return context

    def form_valid(self, form):
        # Attach the status message to the profile
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        # After submission, redirect to the profile page
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})