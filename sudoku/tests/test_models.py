"""
Tests for Sudoku Puzzle model.
"""

import pytest
from django.core.exceptions import ValidationError
from sudoku.models import Puzzle


@pytest.mark.django_db
class TestPuzzleModel:
    """Test Puzzle model."""

    def test_create_puzzle_with_defaults(self):
        """Test creating puzzle with default values."""
        puzzle = Puzzle.objects.create()

        assert puzzle.id is not None
        assert len(puzzle.puzzle) == 81
        assert len(puzzle.solution) == 81
        assert len(puzzle.current_state) == 81
        assert puzzle.difficulty in ['easy', 'medium', 'hard', 'expert']
        assert puzzle.status == 'active'
        assert puzzle.created_at is not None
        assert puzzle.updated_at is not None

    def test_create_puzzle_easy(self):
        """Test creating easy puzzle."""
        puzzle = Puzzle.objects.create(difficulty='easy')

        assert puzzle.difficulty == 'easy'
        # Easy puzzles should have 40-45 clues
        clue_count = sum(1 for cell in puzzle.puzzle if cell != 0)
        assert 40 <= clue_count <= 45

    def test_create_puzzle_medium(self):
        """Test creating medium puzzle."""
        puzzle = Puzzle.objects.create(difficulty='medium')

        assert puzzle.difficulty == 'medium'
        clue_count = sum(1 for cell in puzzle.puzzle if cell != 0)
        assert 30 <= clue_count <= 35

    def test_create_puzzle_hard(self):
        """Test creating hard puzzle."""
        puzzle = Puzzle.objects.create(difficulty='hard')

        assert puzzle.difficulty == 'hard'
        clue_count = sum(1 for cell in puzzle.puzzle if cell != 0)
        assert 25 <= clue_count <= 30

    def test_create_puzzle_expert(self):
        """Test creating expert puzzle."""
        puzzle = Puzzle.objects.create(difficulty='expert')

        assert puzzle.difficulty == 'expert'
        clue_count = sum(1 for cell in puzzle.puzzle if cell != 0)
        assert 22 <= clue_count <= 25

    def test_current_state_initialized_from_puzzle(self):
        """Test that current_state is initialized as copy of puzzle."""
        puzzle = Puzzle.objects.create(difficulty='easy')

        assert puzzle.current_state == puzzle.puzzle

    def test_puzzle_has_valid_solution(self):
        """Test that generated solution is valid."""
        puzzle = Puzzle.objects.create()

        from sudoku import validator
        assert validator.check_solution(puzzle.solution) is True

    def test_puzzle_str_representation(self):
        """Test string representation of puzzle."""
        puzzle = Puzzle.objects.create(difficulty='hard')

        str_repr = str(puzzle)
        assert 'hard' in str_repr.lower()
        assert 'active' in str_repr.lower()


@pytest.mark.django_db
class TestPuzzleMakeMove:
    """Test make_move method."""

    def test_make_valid_move(self):
        """Test making a valid move."""
        puzzle = Puzzle.objects.create()

        # Find first empty cell
        empty_idx = puzzle.current_state.index(0)
        row = empty_idx // 9
        col = empty_idx % 9

        # Get correct value from solution
        correct_value = puzzle.solution[empty_idx]

        success, message = puzzle.make_move(row, col, correct_value)

        assert success is True
        assert message == ""
        assert puzzle.current_state[empty_idx] == correct_value

    def test_make_move_on_filled_cell(self):
        """Test that cannot change pre-filled clue."""
        puzzle = Puzzle.objects.create()

        # Find first clue cell
        filled_idx = next(i for i, v in enumerate(puzzle.puzzle) if v != 0)
        row = filled_idx // 9
        col = filled_idx % 9

        success, message = puzzle.make_move(row, col, 5)

        assert success is False
        assert "cannot change" in message.lower()

    def test_make_invalid_move_row_conflict(self):
        """Test move that violates row rule."""
        puzzle = Puzzle.objects.create()

        # Find first clue
        filled_idx = next(i for i, v in enumerate(puzzle.puzzle) if v != 0)
        filled_row = filled_idx // 9
        filled_value = puzzle.puzzle[filled_idx]

        # Try to place same value in same row
        for col in range(9):
            idx = filled_row * 9 + col
            if puzzle.current_state[idx] == 0:
                success, message = puzzle.make_move(filled_row, col, filled_value)
                assert success is False
                assert "row" in message.lower()
                break

    def test_make_move_out_of_bounds(self):
        """Test move with invalid coordinates."""
        puzzle = Puzzle.objects.create()

        success, message = puzzle.make_move(10, 5, 5)
        assert success is False
        assert "invalid" in message.lower()

        success, message = puzzle.make_move(5, -1, 5)
        assert success is False
        assert "invalid" in message.lower()

    def test_make_move_invalid_value(self):
        """Test move with invalid value."""
        puzzle = Puzzle.objects.create()

        success, message = puzzle.make_move(0, 0, 10)
        assert success is False
        assert "invalid" in message.lower()

        success, message = puzzle.make_move(0, 0, 0)
        assert success is False
        assert "invalid" in message.lower()


@pytest.mark.django_db
class TestPuzzleCheckSolution:
    """Test check_solution method."""

    def test_check_incomplete_solution(self):
        """Test checking incomplete puzzle."""
        puzzle = Puzzle.objects.create()

        is_complete, is_correct, errors = puzzle.check_solution()

        assert is_complete is False
        assert is_correct is False

    def test_check_complete_correct_solution(self):
        """Test checking complete correct solution."""
        puzzle = Puzzle.objects.create()

        # Fill in complete solution
        puzzle.current_state = puzzle.solution.copy()
        puzzle.save()

        is_complete, is_correct, errors = puzzle.check_solution()

        assert is_complete is True
        assert is_correct is True
        assert len(errors) == 0
        assert puzzle.status == 'completed'

    def test_check_complete_incorrect_solution(self):
        """Test checking complete but incorrect solution."""
        puzzle = Puzzle.objects.create()

        # Fill in solution but swap two non-clue cells
        puzzle.current_state = puzzle.solution.copy()

        # Find two empty cells and swap their correct values
        empty_cells = [i for i in range(81) if puzzle.puzzle[i] == 0]
        if len(empty_cells) >= 2:
            idx1, idx2 = empty_cells[0], empty_cells[1]
            puzzle.current_state[idx1], puzzle.current_state[idx2] = \
                puzzle.current_state[idx2], puzzle.current_state[idx1]

        puzzle.save()

        is_complete, is_correct, errors = puzzle.check_solution()

        assert is_complete is True
        assert is_correct is False
        assert len(errors) > 0


@pytest.mark.django_db
class TestPuzzleGetHint:
    """Test get_hint method."""

    def test_get_hint_returns_empty_cell(self):
        """Test that hint returns an empty cell with correct value."""
        puzzle = Puzzle.objects.create()

        row, col, value = puzzle.get_hint()

        # Check coordinates are valid
        assert 0 <= row < 9
        assert 0 <= col < 9

        # Check cell is empty
        idx = row * 9 + col
        assert puzzle.current_state[idx] == 0

        # Check value is correct
        assert value == puzzle.solution[idx]

    def test_get_hint_on_completed_puzzle(self):
        """Test getting hint when puzzle is complete."""
        puzzle = Puzzle.objects.create()

        # Complete the puzzle
        puzzle.current_state = puzzle.solution.copy()
        puzzle.save()

        row, col, value = puzzle.get_hint()

        # Should return None values when no empty cells
        assert row is None
        assert col is None
        assert value is None

    def test_multiple_hints_give_different_cells(self):
        """Test that multiple hints provide variety."""
        puzzle = Puzzle.objects.create()

        hint1 = puzzle.get_hint()
        hint2 = puzzle.get_hint()
        hint3 = puzzle.get_hint()

        # All should be valid
        for row, col, value in [hint1, hint2, hint3]:
            assert 0 <= row < 9
            assert 0 <= col < 9
            idx = row * 9 + col
            assert value == puzzle.solution[idx]


@pytest.mark.django_db
class TestPuzzleReset:
    """Test reset method."""

    def test_reset_puzzle(self):
        """Test resetting puzzle to initial state."""
        puzzle = Puzzle.objects.create()

        # Make some moves
        empty_cells = [i for i in range(81) if puzzle.puzzle[i] == 0]
        for idx in empty_cells[:5]:
            row = idx // 9
            col = idx % 9
            puzzle.make_move(row, col, puzzle.solution[idx])

        # Verify moves were made
        assert puzzle.current_state != puzzle.puzzle

        # Reset
        puzzle.reset()

        # Verify reset to original
        assert puzzle.current_state == puzzle.puzzle
        assert puzzle.status == 'active'


@pytest.mark.django_db
class TestPuzzleQueryMethods:
    """Test model query methods."""

    def test_filter_by_difficulty(self):
        """Test filtering puzzles by difficulty."""
        Puzzle.objects.create(difficulty='easy')
        Puzzle.objects.create(difficulty='easy')
        Puzzle.objects.create(difficulty='hard')

        easy_puzzles = Puzzle.objects.filter(difficulty='easy')
        assert easy_puzzles.count() == 2

    def test_filter_by_status(self):
        """Test filtering puzzles by status."""
        p1 = Puzzle.objects.create()
        p2 = Puzzle.objects.create()

        # Complete one puzzle
        p1.current_state = p1.solution.copy()
        p1.status = 'completed'
        p1.save()

        active_puzzles = Puzzle.objects.filter(status='active')
        completed_puzzles = Puzzle.objects.filter(status='completed')

        assert active_puzzles.count() == 1
        assert completed_puzzles.count() == 1
