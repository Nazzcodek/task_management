#!/usr/bin/env python3
"""This module defines the Task model."""
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Represents a task in the system.
    
    Attributes:
        title (str): The title of the task.
        description (str): The description of the task.
        status (str): The status of the task.
            - chices: In Progress, Completed, Overdue
        priority (str): The priority of the task.
            - choices: Low, Medium, High
        due_date (datetime): The due date of the task.
        category (str): The category of the task.
        assigned_to (User): The user assigned to the task.
    """
    STATUS = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Overdue', 'Overdue'),
    ]

    PRIORITY = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS)
    priority = models.CharField(max_length=20, choices=PRIORITY)
    due_date = models.DateTimeField()
    category = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

