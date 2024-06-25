#!/usr/bin/env python3
"""This module defines the helper functions for the user app."""
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


def add_new_user(request):
    """
    Adds a new user to the system.

    Args:
        request (HttpRequest): The HTTP request object containing the user data.

    Returns:
        Response: A JSON response with the status of the user creation. If the user data is valid and the password is validated successfully, the response contains the user's id and username. If the user data is invalid, the response contains an error message and the details of the validation errors. If the password validation fails, the response contains an error message and the details of the validation errors.

    Raises:
        Exception: If an internal server error occurs during password validation.

    Example:
        {
            "id": 1,
            "username": "user1"
        }

        {
            "error": "Validation errors occurred",
            "details": {
                "email": "This field is required."
            }
        }

        {
            "error": "Password validation failed",
            "details": [
                "This password is too short. It must contain at least 8 characters."
            ]
        }
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        try:
            validate_password(password)
        except Exception as e:
            error_messages = [str(err) for err in e.error_list]
            return Response({'error': 'Password validation failed', 'details': error_messages}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
    else:
        error_details = {field: error[0].__str__() for field, error in serializer.errors.items()}
        return Response({'error': 'Validation errors occurred', 'details': error_details}, status=status.HTTP_400_BAD_REQUEST)