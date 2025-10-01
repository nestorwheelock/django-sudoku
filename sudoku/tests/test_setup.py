"""
Tests for basic sudoku app setup and configuration.
"""

import pytest
from django.apps import apps
from django.conf import settings


def test_package_imports():
    """Test that sudoku package can be imported."""
    import sudoku
    assert sudoku.__version__ == "1.0.0"


def test_package_version():
    """Test package version is correctly set."""
    from sudoku import __version__
    assert __version__ == "1.0.0"


def test_app_config_exists():
    """Test that SudokuConfig is registered."""
    app_config = apps.get_app_config("sudoku")
    assert app_config.name == "sudoku"
    assert app_config.verbose_name == "Sudoku Puzzle Game"


def test_url_configuration_loads():
    """Test that URL configuration can be imported."""
    from sudoku import urls
    assert hasattr(urls, "urlpatterns")
    assert hasattr(urls, "app_name")
    assert urls.app_name == "sudoku"


def test_models_module_exists():
    """Test that models module exists."""
    from sudoku import models
    assert models is not None


def test_views_module_exists():
    """Test that views module exists."""
    from sudoku import views
    assert views is not None


def test_admin_module_exists():
    """Test that admin module exists."""
    from sudoku import admin
    assert admin is not None


def test_migrations_directory_exists():
    """Test that migrations directory exists."""
    import os
    from sudoku import __file__ as sudoku_init
    sudoku_dir = os.path.dirname(sudoku_init)
    migrations_dir = os.path.join(sudoku_dir, "migrations")
    assert os.path.exists(migrations_dir)
    assert os.path.exists(os.path.join(migrations_dir, "__init__.py"))


def test_templates_directory_exists():
    """Test that templates directory exists."""
    import os
    from sudoku import __file__ as sudoku_init
    sudoku_dir = os.path.dirname(sudoku_init)
    templates_dir = os.path.join(sudoku_dir, "templates", "sudoku")
    assert os.path.exists(templates_dir)


def test_static_directory_exists():
    """Test that static directory exists."""
    import os
    from sudoku import __file__ as sudoku_init
    sudoku_dir = os.path.dirname(sudoku_init)
    static_dir = os.path.join(sudoku_dir, "static", "sudoku")
    assert os.path.exists(static_dir)


def test_tests_directory_exists():
    """Test that tests directory exists."""
    import os
    from sudoku import __file__ as sudoku_init
    sudoku_dir = os.path.dirname(sudoku_init)
    tests_dir = os.path.join(sudoku_dir, "tests")
    assert os.path.exists(tests_dir)
    assert os.path.exists(os.path.join(tests_dir, "__init__.py"))
