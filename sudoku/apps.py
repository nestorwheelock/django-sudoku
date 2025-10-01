from django.apps import AppConfig


class SudokuConfig(AppConfig):
    """Django app configuration for sudoku."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "sudoku"
    verbose_name = "Sudoku Puzzle Game"
