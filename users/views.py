#!/usr/bin/env python3
"""This module defines the UserViewSet class and signup and login logic."""
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from .services import add_new_user


def signup(request):
    """
    Signup view function that handles the creation of a new user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: If the request method is POST and the form is valid,
        redirects the user to the tasks:index page with a token query parameter.
        If the request method is not POST, renders the signup.html template with
        an instance of the CustomUserCreationForm.

    Raises:
        None

    Example:
        POST request with valid form data:
            Redirects to tasks:index with a token query parameter.

        POST request with invalid form data:
            Renders the signup.html template with the form and error messages.

        GET request:
            Renders the signup.html template with an instance of the
            CustomUserCreationForm.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            redirect_url = reverse('tasks:index') + f'?token={token.key}'
            return redirect(redirect_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """
    Handles the login view logic based on the request method.
    If the request method is POST, 
    validates the CustomAuthenticationForm and logs in the user.
    Then, creates a token for the user and 
    redirectsto the tasks:index page with the token query parameter. 
    If the request method is not POST, renders the login.html
    template with the CustomAuthenticationForm.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: If the request method is POST and the form is valid,
        redirects the user to the tasks:index page with a token query parameter.
        If the request method is not POST, renders the
        login.html template with the CustomAuthenticationForm.
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            redirect_url = reverse('tasks:index') + f'?token={token.key}'
            return redirect(redirect_url)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


class UserViewSet(ViewSet):
    """
    Viewset for managing users. Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Retrieves a list of all users and returns their data in a JSON response.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A JSON response containing a list of dictionaries,
            where each dictionary represents a user and contains the user's id and name.
        """
        users = User.objects.all()
        user_data = [{'id': user.id, 'name': user.username} for user in users]
        return Response(user_data)

    @action(detail=False, methods=['get'])
    def get_user_info(self, request):
        """
        Retrieves information about the first 5 users and the total number of users.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A JSON response containing a list of dictionaries,
            where each dictionary represents a user and contains the user's id and username.
            Additionally, the total number of users is included in the response.

        Example:
            {
                "users": [
                    {
                        "id": 1,
                        "username": "user1"
                    },
                    {
                        "id": 2,
                        "username": "user2"
                    },
                ],
                "total": 10
            }
        """
        users = User.objects.all()[:5]
        user_info = [{'id': user.id, 'username': user.username} for user in users]
        total_users = User.objects.count()
        return Response({'users': user_info, 'total': total_users}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def add_user(self, request):
        """
        Adds a new user to the system.

        Parameters:
            request (HttpRequest): The HTTP request object containing the user data.

        Returns:
            Response: A JSON response with the status of the user creation.

        Example:
            {
                "status": "success"
            }
        """
        return add_new_user(request)