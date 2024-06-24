#!/usr/bin/env python3
"""This module defines the TaskTests class."""
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task
from django.utils import timezone
from rest_framework.authtoken.models import Token


class TaskTests(APITestCase):
    """
    This class tests the Task API endpoints.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user and token, then
        creating a task for testing.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='In Progress',
            priority='Medium',
            due_date=timezone.now() + timezone.timedelta(days=1),
            category='Test Category',
            assigned_to=self.user
        )

    def test_get_all_tasks(self):
        """
        Test the GET request to retrieve all tasks.
        """
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tasks_by_status(self):
        """
        Test the GET request to retrieve tasks by status.
        """
        response = self.client.get('/api/v1/tasks/status/In Progress/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')

    def test_create_task(self):
        """
        Test the POST request to create a new task.
        """
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'status': 'In Progress',
            'priority': 'High',
            'due_date': (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            'category': 'New Category',
            'assigned_to': self.user.id
        }
        response = self.client.post('/api/v1/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(id=response.data['id']).title, 'New Task')

    def test_update_task(self):
        """
        Test the PUT request to update an existing task.
        """
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': 'Completed',
            'priority': 'Low',
            'due_date': (timezone.now() + timezone.timedelta(days=3)).isoformat(),
            'category': 'Updated Category',
            'assigned_to': self.user.id
        }
        response = self.client.put(f'/api/v1/tasks/{self.task.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'Completed')

    def test_retrieve_task(self):
        """
        Test the GET request to retrieve a specific task.
        """
        response = self.client.get(f'/api/v1/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_delete_task(self):
        """
        Test the DELETE request to delete a task.
        """
        response = self.client.delete(f'/api/v1/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
