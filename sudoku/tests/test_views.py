"""
Tests for Sudoku template views.
"""

import pytest
from django.urls import reverse
from sudoku.models import Puzzle


@pytest.mark.django_db
class TestPuzzleListView:
    """Test puzzle list template view."""

    def test_puzzle_list_view_renders(self, client):
        """Test that puzzle list view renders successfully."""
        response = client.get(reverse('sudoku:puzzle_list'))

        assert response.status_code == 200
        assert 'sudoku/puzzle_list.html' in [t.name for t in response.templates]

    def test_puzzle_list_displays_puzzles(self, client):
        """Test that puzzles are displayed in list."""
        Puzzle.objects.create(difficulty='easy')
        Puzzle.objects.create(difficulty='hard')

        response = client.get(reverse('sudoku:puzzle_list'))

        assert response.status_code == 200
        assert b'easy' in response.content.lower()
        assert b'hard' in response.content.lower()

    def test_puzzle_list_empty(self, client):
        """Test puzzle list when no puzzles exist."""
        response = client.get(reverse('sudoku:puzzle_list'))

        assert response.status_code == 200
        assert len(response.context['puzzles']) == 0


@pytest.mark.django_db
class TestPuzzleCreateView:
    """Test puzzle creation view."""

    def test_puzzle_create_view_get(self, client):
        """Test GET request to create puzzle page."""
        response = client.get(reverse('sudoku:puzzle_create'))

        assert response.status_code == 200
        assert 'sudoku/puzzle_create.html' in [t.name for t in response.templates]

    def test_puzzle_create_view_post(self, client):
        """Test POST request to create puzzle."""
        response = client.post(
            reverse('sudoku:puzzle_create'),
            {'difficulty': 'medium'}
        )

        assert response.status_code == 302  # Redirect
        assert Puzzle.objects.count() == 1
        puzzle = Puzzle.objects.first()
        assert puzzle.difficulty == 'medium'

    def test_puzzle_create_redirects_to_play(self, client):
        """Test that creating puzzle redirects to play view."""
        response = client.post(
            reverse('sudoku:puzzle_create'),
            {'difficulty': 'easy'}
        )

        puzzle = Puzzle.objects.first()
        assert response.status_code == 302
        assert response.url == reverse('sudoku:puzzle_play', args=[puzzle.id])


@pytest.mark.django_db
class TestPuzzlePlayView:
    """Test puzzle play view."""

    def test_puzzle_play_view_renders(self, client):
        """Test that play view renders successfully."""
        puzzle = Puzzle.objects.create(difficulty='medium')

        response = client.get(reverse('sudoku:puzzle_play', args=[puzzle.id]))

        assert response.status_code == 200
        assert 'sudoku/puzzle_play.html' in [t.name for t in response.templates]

    def test_puzzle_play_view_context(self, client):
        """Test that play view has correct context."""
        puzzle = Puzzle.objects.create(difficulty='hard')

        response = client.get(reverse('sudoku:puzzle_play', args=[puzzle.id]))

        assert response.status_code == 200
        assert 'puzzle' in response.context
        assert response.context['puzzle'].id == puzzle.id

    def test_puzzle_play_nonexistent_puzzle(self, client):
        """Test play view with non-existent puzzle."""
        response = client.get(reverse('sudoku:puzzle_play', args=[99999]))

        assert response.status_code == 404

    def test_puzzle_play_provides_api_base_url_in_template(self, client):
        """
        Test that play view template provides apiBaseUrl to JavaScript.

        Regression test for bugs #8, #9, #10, #11.
        JavaScript needs the correct API base URL to make fetch requests.
        """
        puzzle = Puzzle.objects.create(difficulty='easy')
        response = client.get(reverse('sudoku:puzzle_play', args=[puzzle.id]))

        assert response.status_code == 200
        # Check that apiBaseUrl variable is defined in the page
        assert b'apiBaseUrl' in response.content
        # Check that it contains the API path
        assert b'/api/puzzles' in response.content


@pytest.mark.django_db
class TestPuzzleDeleteView:
    """Test puzzle deletion view."""

    def test_puzzle_delete_view_post(self, client):
        """Test POST request to delete puzzle."""
        puzzle = Puzzle.objects.create(difficulty='easy')

        response = client.post(reverse('sudoku:puzzle_delete', args=[puzzle.id]))

        assert response.status_code == 302  # Redirect
        assert Puzzle.objects.count() == 0

    def test_puzzle_delete_redirects_to_list(self, client):
        """Test that deleting puzzle redirects to list."""
        puzzle = Puzzle.objects.create(difficulty='medium')

        response = client.post(reverse('sudoku:puzzle_delete', args=[puzzle.id]))

        assert response.status_code == 302
        assert response.url == reverse('sudoku:puzzle_list')
