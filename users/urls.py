#!/usr/bin/env python3
"""This module defines the urls for the users app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


app_name = 'users'
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('api/v1/', include(router.urls)),
]