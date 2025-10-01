"""
Test URL configuration.
"""

from django.urls import path, include

urlpatterns = [
    path('', include('sudoku.urls')),
]
