from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

class TestLoginView(View):
    """Test login endpoint for debugging"""
    
    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Try to authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': f'Logged in as {user.username}',
                'user': user.username,
                'is_authenticated': request.user.is_authenticated
            })
        else:
            # Check if user exists
            user_exists = User.objects.filter(username=username).exists()
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid username or password',
                'user_exists': user_exists,
                'username_provided': username
            })
    
    def get(self, request):
        return JsonResponse({
            'message': 'Test login endpoint',
            'current_user': request.user.username if request.user.is_authenticated else 'Anonymous',
            'is_authenticated': request.user.is_authenticated,
            'available_users': list(User.objects.values_list('username', flat=True))
        })
