#!/usr/bin/env python3
"""This module defines the TaskViewSet class."""
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from .services import get_tasks_by_status, create_task, update_task
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.shortcuts import render


def index(request):
    """
    Render the index.html template.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTTP response.
    """

    return render(request, 'tasks/index.html')


class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task instances.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a new task instance.

        Parameters:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response containing the serialized task data and a status code.

        Raises:
            ValidationError: If the request data fails validation.
            Exception: If an internal server error occurs.
        """
        try:
            serializer = create_task(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    def update(self, request, *args, **kwargs):
        """
        Update a task instance based on the provided request data.

        Parameters:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response containing the serialized task data and a status code.

        Raises:
            ValidationError: If the request data fails validation.
            Exception: If an internal server error occurs.
        """
        try:
            task = self.get_object()
            serializer = update_task(task, request.data)
            return Response(serializer.data)
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    @action(detail=False, methods=['get'], url_path='status/(?P<status>[^/.]+)')
    def tasks_by_status(self, request, status=None):
        """
        Retrieve tasks by status and serialize the data to be returned in the response.
        
        Parameters:
            self: The TaskViewSet instance.
            request (Request): The HTTP request object.
            status (str, optional): The status to filter tasks by.

        Returns:
            Response: The HTTP response containing the serialized task data.

        Raises:
            Exception: If an internal server error occurs.
        """
        try:
            tasks = get_tasks_by_status(status)
            serializer = self.get_serializer(tasks, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
