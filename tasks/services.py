#!/usr/bin/env python3
"""This module defines the helper functions for the task app"""
from .models import Task
from .serializers import TaskSerializer
from rest_framework.exceptions import ValidationError

def create_task(request_data):
    """
    Create a task based on the provided request data.

    Parameters:
        request_data (dict): The request data containing task details.

    Returns:
        TaskSerializer: The serializer containing the created task.
    """
    serializer = TaskSerializer(data=request_data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer
    else:
        raise ValidationError(serializer.errors)

def update_task(task, request_data):
    """
    Update a task based on the provided request data.

    Parameters:
        task (Task): The task instance to update.
        request_data (dict): The request data containing task details.

    Returns:
        TaskSerializer: The serializer containing the updated task.
    """
    serializer = TaskSerializer(task, data=request_data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer
    else:
        raise ValidationError(serializer.errors)

def get_tasks_by_status(status):
    """
    Retrieve tasks by their status.

    Parameters:
        status (str): The status to filter tasks by.

    Returns:
        QuerySet: A queryset of tasks filtered by the given status.
    """
    return Task.objects.filter(status=status)
