#!/usr/bin/env python3
"""This module defines the get_tasks_by_status function."""
from .models import Task

def get_tasks_by_status(status):
    """
    Retrieve tasks by their status.
    :param status: The status of the tasks to retrieve.
    :return: QuerySet of tasks with the given status.
    """
    return Task.objects.filter(status=status)
