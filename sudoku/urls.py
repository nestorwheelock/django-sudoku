from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PuzzleViewSet

app_name = "sudoku"

router = DefaultRouter()
router.register(r'puzzles', PuzzleViewSet, basename='puzzle')

urlpatterns = [
    path("api/", include(router.urls)),
]
