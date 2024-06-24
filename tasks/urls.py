#!/usr/bin/env python3
"""This module defines the urls for the tasks app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, index


app_name = 'tasks'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/', index, name='index'),
]
