"""
Tests for Sudoku REST API endpoints.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from sudoku.models import Puzzle


@pytest.fixture
def api_client():
    """Create API client for testing."""
    return APIClient()


@pytest.fixture
def sample_puzzle():
    """Create a sample puzzle for testing."""
    return Puzzle.objects.create(difficulty='medium')


@pytest.mark.django_db
class TestPuzzleListCreate:
    """Test GET /api/puzzles/ and POST /api/puzzles/"""

    def test_list_puzzles(self, api_client):
        """Test listing all puzzles."""
        # Create some puzzles
        Puzzle.objects.create(difficulty='easy')
        Puzzle.objects.create(difficulty='hard')

        response = api_client.get('/api/puzzles/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_list_puzzles_empty(self, api_client):
        """Test listing when no puzzles exist."""
        response = api_client.get('/api/puzzles/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_create_puzzle_default_difficulty(self, api_client):
        """Test creating puzzle with default difficulty."""
        response = api_client.post('/api/puzzles/', {})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['difficulty'] == 'medium'
        assert response.data['status'] == 'active'
        assert 'id' in response.data
        assert 'puzzle' in response.data
        assert 'current_state' in response.data
        assert len(response.data['puzzle']) == 81

    def test_create_puzzle_with_difficulty(self, api_client):
        """Test creating puzzle with specified difficulty."""
        response = api_client.post('/api/puzzles/', {'difficulty': 'hard'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['difficulty'] == 'hard'

        # Verify clue count matches difficulty
        clue_count = sum(1 for cell in response.data['puzzle'] if cell != 0)
        assert 25 <= clue_count <= 30

    def test_create_puzzle_invalid_difficulty(self, api_client):
        """Test creating puzzle with invalid difficulty."""
        response = api_client.post('/api/puzzles/', {'difficulty': 'impossible'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_solution_not_exposed_in_list(self, api_client):
        """Test that solution field is not exposed in list endpoint."""
        Puzzle.objects.create(difficulty='easy')

        response = api_client.get('/api/puzzles/')

        assert response.status_code == status.HTTP_200_OK
        assert 'solution' not in response.data[0]


@pytest.mark.django_db
class TestPuzzleDetail:
    """Test GET /api/puzzles/{id}/"""

    def test_retrieve_puzzle(self, api_client, sample_puzzle):
        """Test retrieving a specific puzzle."""
        response = api_client.get(f'/api/puzzles/{sample_puzzle.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_puzzle.id
        assert response.data['difficulty'] == 'medium'
        assert response.data['status'] == 'active'
        assert 'puzzle' in response.data
        assert 'current_state' in response.data

    def test_retrieve_nonexistent_puzzle(self, api_client):
        """Test retrieving puzzle that doesn't exist."""
        response = api_client.get('/api/puzzles/99999/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_solution_not_exposed_in_detail(self, api_client, sample_puzzle):
        """Test that solution field is not exposed in detail endpoint."""
        response = api_client.get(f'/api/puzzles/{sample_puzzle.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert 'solution' not in response.data


@pytest.mark.django_db
class TestPuzzleMove:
    """Test POST /api/puzzles/{id}/move/"""

    def test_make_valid_move(self, api_client, sample_puzzle):
        """Test making a valid move."""
        # Find first empty cell
        empty_idx = sample_puzzle.current_state.index(0)
        row = empty_idx // 9
        col = empty_idx % 9
        value = sample_puzzle.solution[empty_idx]

        response = api_client.post(
            f'/api/puzzles/{sample_puzzle.id}/move/',
            {'row': row, 'col': col, 'value': value}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['message'] == ""
        assert response.data['current_state'][empty_idx] == value

    def test_make_invalid_move_row_conflict(self, api_client, sample_puzzle):
        """Test move that violates row rule."""
        # Find a clue cell
        filled_idx = next(i for i, v in enumerate(sample_puzzle.puzzle) if v != 0)
        filled_row = filled_idx // 9
        filled_value = sample_puzzle.puzzle[filled_idx]

        # Try to place same value in same row
        for col in range(9):
            idx = filled_row * 9 + col
            if sample_puzzle.current_state[idx] == 0:
                response = api_client.post(
                    f'/api/puzzles/{sample_puzzle.id}/move/',
                    {'row': filled_row, 'col': col, 'value': filled_value}
                )

                assert response.status_code == status.HTTP_400_BAD_REQUEST
                assert response.data['success'] is False
                assert 'row' in response.data['message'].lower()
                break

    def test_make_move_on_clue_cell(self, api_client, sample_puzzle):
        """Test that cannot change pre-filled clue."""
        # Find a clue cell
        filled_idx = next(i for i, v in enumerate(sample_puzzle.puzzle) if v != 0)
        row = filled_idx // 9
        col = filled_idx % 9

        response = api_client.post(
            f'/api/puzzles/{sample_puzzle.id}/move/',
            {'row': row, 'col': col, 'value': 5}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False
        assert 'cannot change' in response.data['message'].lower()

    def test_make_move_missing_parameters(self, api_client, sample_puzzle):
        """Test move with missing parameters."""
        response = api_client.post(
            f'/api/puzzles/{sample_puzzle.id}/move/',
            {'row': 0, 'col': 0}  # missing 'value'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_make_move_invalid_coordinates(self, api_client, sample_puzzle):
        """Test move with out-of-bounds coordinates."""
        response = api_client.post(
            f'/api/puzzles/{sample_puzzle.id}/move/',
            {'row': 10, 'col': 5, 'value': 5}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPuzzleCheck:
    """Test POST /api/puzzles/{id}/check/"""

    def test_check_incomplete_puzzle(self, api_client, sample_puzzle):
        """Test checking incomplete puzzle."""
        response = api_client.post(f'/api/puzzles/{sample_puzzle.id}/check/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['complete'] is False
        assert response.data['correct'] is False

    def test_check_complete_correct_solution(self, api_client, sample_puzzle):
        """Test checking complete correct solution."""
        # Fill in complete solution
        sample_puzzle.current_state = sample_puzzle.solution.copy()
        sample_puzzle.save()

        response = api_client.post(f'/api/puzzles/{sample_puzzle.id}/check/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['complete'] is True
        assert response.data['correct'] is True
        assert len(response.data['errors']) == 0

    def test_check_complete_incorrect_solution(self, api_client, sample_puzzle):
        """Test checking complete but incorrect solution."""
        # Fill in solution but swap two cells
        sample_puzzle.current_state = sample_puzzle.solution.copy()
        empty_cells = [i for i in range(81) if sample_puzzle.puzzle[i] == 0]
        if len(empty_cells) >= 2:
            idx1, idx2 = empty_cells[0], empty_cells[1]
            sample_puzzle.current_state[idx1], sample_puzzle.current_state[idx2] = \
                sample_puzzle.current_state[idx2], sample_puzzle.current_state[idx1]
        sample_puzzle.save()

        response = api_client.post(f'/api/puzzles/{sample_puzzle.id}/check/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['complete'] is True
        assert response.data['correct'] is False
        assert len(response.data['errors']) > 0


@pytest.mark.django_db
class TestPuzzleHint:
    """Test POST /api/puzzles/{id}/hint/"""

    def test_get_hint(self, api_client, sample_puzzle):
        """Test getting a hint."""
        response = api_client.post(f'/api/puzzles/{sample_puzzle.id}/hint/')

        assert response.status_code == status.HTTP_200_OK
        assert 'row' in response.data
        assert 'col' in response.data
        assert 'value' in response.data

        # Verify hint is valid
        row = response.data['row']
        col = response.data['col']
        value = response.data['value']
        idx = row * 9 + col

        assert 0 <= row < 9
        assert 0 <= col < 9
        assert sample_puzzle.current_state[idx] == 0
        assert value == sample_puzzle.solution[idx]

    def test_get_hint_on_completed_puzzle(self, api_client, sample_puzzle):
        """Test getting hint when puzzle is complete."""
        sample_puzzle.current_state = sample_puzzle.solution.copy()
        sample_puzzle.save()

        response = api_client.post(f'/api/puzzles/{sample_puzzle.id}/hint/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['row'] is None
        assert response.data['col'] is None
        assert response.data['value'] is None


@pytest.mark.django_db
class TestPuzzleReset:
    """Test POST /api/puzzles/{id}/reset/"""

    def test_reset_puzzle(self, api_client, sample_puzzle):
        """Test resetting puzzle to initial state."""
        # Make some moves
        empty_cells = [i for i in range(81) if sample_puzzle.puzzle[i] == 0]
        for idx in empty_cells[:3]:
            row = idx // 9
            col = idx % 9
            sample_puzzle.make_move(row, col, sample_puzzle.solution[idx])

        # Verify moves were made
        assert sample_puzzle.current_state != sample_puzzle.puzzle

        response = api_client.post(f'/api/puzzles/{sample_puzzle.id}/reset/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == "Puzzle reset to initial state"

        # Verify puzzle was reset
        sample_puzzle.refresh_from_db()
        assert sample_puzzle.current_state == sample_puzzle.puzzle
        assert sample_puzzle.status == 'active'


@pytest.mark.django_db
class TestPuzzleDelete:
    """Test DELETE /api/puzzles/{id}/"""

    def test_delete_puzzle(self, api_client, sample_puzzle):
        """Test deleting a puzzle."""
        puzzle_id = sample_puzzle.id

        response = api_client.delete(f'/api/puzzles/{puzzle_id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify puzzle is deleted
        assert not Puzzle.objects.filter(id=puzzle_id).exists()

    def test_delete_nonexistent_puzzle(self, api_client):
        """Test deleting puzzle that doesn't exist."""
        response = api_client.delete('/api/puzzles/99999/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestFilteringAndOrdering:
    """Test filtering and ordering puzzles."""

    def test_filter_by_difficulty(self, api_client):
        """Test filtering puzzles by difficulty."""
        Puzzle.objects.create(difficulty='easy')
        Puzzle.objects.create(difficulty='easy')
        Puzzle.objects.create(difficulty='hard')

        response = api_client.get('/api/puzzles/?difficulty=easy')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert all(p['difficulty'] == 'easy' for p in response.data)

    def test_filter_by_status(self, api_client):
        """Test filtering puzzles by status."""
        p1 = Puzzle.objects.create()
        p2 = Puzzle.objects.create()

        # Complete one puzzle
        p1.current_state = p1.solution.copy()
        p1.status = 'completed'
        p1.save()

        response = api_client.get('/api/puzzles/?status=completed')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['status'] == 'completed'

    def test_ordering_by_created_at(self, api_client):
        """Test that puzzles are ordered by creation time (newest first)."""
        p1 = Puzzle.objects.create(difficulty='easy')
        p2 = Puzzle.objects.create(difficulty='hard')

        response = api_client.get('/api/puzzles/')

        assert response.status_code == status.HTTP_200_OK
        # Newest first (p2)
        assert response.data[0]['id'] == p2.id
        assert response.data[1]['id'] == p1.id
