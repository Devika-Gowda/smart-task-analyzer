"""
Main URL router of the backend.
We only expose /api/tasks/ to keep structure clean.
"""
from django.urls import path, include

urlpatterns = [
    path("api/tasks/", include("tasks.urls")),  # Includes app-level routes
]
