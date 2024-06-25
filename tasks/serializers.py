#!/usr/bin/env python3
"""This module defines the TaskSerializer class."""
from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task instances.

    This serializer maps the Task model to JSON format.

    Attributes:
        assigned_to (PrimaryKeyRelatedField): The user assigned to the task.

    """
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        error_messages={'incorrect_type': 'Please select a valid user ID.'}
    )

    class Meta:
        model = Task
        fields = '__all__'
