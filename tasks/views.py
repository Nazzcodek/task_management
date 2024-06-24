#!/usr/bin/env python3
"""This module defines the TaskViewSet class."""
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from .services import get_tasks_by_status
from rest_framework.decorators import action
from rest_framework.response import Response


class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task instances.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @action(detail=False, methods=['get'], url_path='status/(?P<status>[^/.]+)')
    def tasks_by_status(self, request, status=None):
        """
        Retrieve tasks by status.
        """
        tasks = get_tasks_by_status(status)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

