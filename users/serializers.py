#!/usr/bin/env python3
"""This module defines the UserSerializer class."""
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for serializing and deserializing User objects.
    """
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        A method that creates a new user instance with the given validated data.

        Args:
            validated_data (dict): A dictionary containing validated user data with 'username' and 'password' keys.

        Returns:
            User: The newly created User instance with the provided username and password.
        """
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
