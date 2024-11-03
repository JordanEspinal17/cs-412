from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView, View,FormView
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm,UpdateStatusMessageForm  
from django.urls import reverse,reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from .forms import UpdateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.db import transaction


class ShowAllProfilesView(ListView):
    model = Profile  # This fetches all profiles from the database
    template_name = 'mini_fb/show_all_profiles.html'  # Template for the view
    context_object_name = 'profiles'  # Context name for the list of profiles

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'


class CreateProfileView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']
    template_name = 'mini_fb/create_profile_form.html'
    success_url = '/mini_fb/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UserRegisterView(FormView):
    template_name = 'mini_fb/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    fields = ['message', 'image']  # Assuming 'image' is a field in your StatusMessage model
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        # Get the profile based on the `pk` from the URL
        profile_pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=profile_pk)
        # Assign the profile to the status message
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the profile page
        profile_pk = self.kwargs.get('pk')
        return reverse('mini_fb:show_profile', kwargs={'pk': profile_pk})

    def get_context_data(self, **kwargs):
        # Pass the profile to the template context
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs.get('pk')
        context['profile'] = Profile.objects.get(pk=profile_pk)
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self, queryset=None):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404("No Profile matches the logged-in user.")

    def get_success_url(self):
        return reverse_lazy('show_my_profile')

    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            raise PermissionDenied("You are not allowed to edit this profile.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Redirect to the profile page of the user who owns the status message
        profile_id = self.object.profile.pk
        return reverse_lazy('show_profile', kwargs={'pk': profile_id})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            raise PermissionDenied("You are not allowed to edit this profile.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Redirect to the profile page of the user who owns the status message
        profile_id = self.object.profile.pk
        return reverse_lazy('show_profile', kwargs={'pk': profile_id})
    
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
            profile.add_friend(other_profile)
            return redirect('show_my_profile')
        except Profile.DoesNotExist:
            raise Http404("No Profile matches the logged-in user.")

    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

    def get_object(self, queryset=None):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404("No Profile matches the logged-in user.")

    
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'

    def get_object(self, queryset=None):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404("No Profile matches the logged-in user.")

    
class ShowMyProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404("No Profile matches the logged-in user.")
