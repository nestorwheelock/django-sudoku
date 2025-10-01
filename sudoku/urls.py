from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "sudoku"

# Router will be configured in T-003
router = DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
]
