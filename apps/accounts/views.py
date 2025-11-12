from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import UserProfile
from .forms import UserRegistrationForm, UserProfileForm


class RegisterView(CreateView):
    """User registration view"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('blog:post-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        password = form.cleaned_data['password']
        self.object.set_password(password)
        self.object.save()
        
        # Create user profile
        UserProfile.objects.get_or_create(user=self.object)
        
        # Log the user in
        login(self.request, self.object)
        messages.success(self.request, 'Registration successful!')
        
        return response


class LoginView(View):
    """User login view"""
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('blog:post-list')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name)


class LogoutView(LoginRequiredMixin, View):
    """User logout view"""
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('blog:post-list')


class ProfileView(LoginRequiredMixin, DetailView):
    """User profile view"""
    model = UserProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit user profile"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
