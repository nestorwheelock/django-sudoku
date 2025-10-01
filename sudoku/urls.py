from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PuzzleViewSet,
    PuzzleListView,
    PuzzleCreateView,
    PuzzlePlayView,
    PuzzleDeleteView,
)

app_name = "sudoku"

router = DefaultRouter()
router.register(r'puzzles', PuzzleViewSet, basename='puzzle')

urlpatterns = [
    # API endpoints
    path("api/", include(router.urls)),

    # Template views
    path("", PuzzleListView.as_view(), name="puzzle_list"),
    path("create/", PuzzleCreateView.as_view(), name="puzzle_create"),
    path("<int:pk>/", PuzzlePlayView.as_view(), name="puzzle_play"),
    path("<int:pk>/delete/", PuzzleDeleteView.as_view(), name="puzzle_delete"),
]
