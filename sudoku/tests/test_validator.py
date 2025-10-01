"""
Tests for Sudoku validation logic.
"""

import pytest
from sudoku import validator


class TestRowValidation:
    """Test row validation."""

    def test_validate_row_with_no_conflict(self):
        """Test valid row with no conflicts."""
        grid = [
            5, 3, 4, 6, 7, 8, 9, 1, 2,  # row 0: all unique
            0, 0, 0, 0, 0, 0, 0, 0, 0,  # rest empty
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert validator.validate_row(grid, 0, 9) is False  # 9 not in row, but row is full
        assert validator.validate_row(grid, 0, 5) is False  # 5 already in row

    def test_validate_row_with_conflict(self):
        """Test row with value conflict."""
        grid = [
            5, 3, 0, 0, 0, 0, 0, 0, 0,  # row 0
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert validator.validate_row(grid, 0, 5) is False  # 5 already exists
        assert validator.validate_row(grid, 0, 3) is False  # 3 already exists
        assert validator.validate_row(grid, 0, 4) is True   # 4 doesn't exist

    def test_validate_row_all_rows(self):
        """Test validation works for all 9 rows."""
        grid = [0] * 81
        grid[0] = 5  # row 0
        grid[18] = 5  # row 2
        grid[36] = 5  # row 4
        grid[54] = 5  # row 6
        grid[72] = 5  # row 8

        assert validator.validate_row(grid, 0, 5) is False
        assert validator.validate_row(grid, 1, 5) is True
        assert validator.validate_row(grid, 2, 5) is False
        assert validator.validate_row(grid, 3, 5) is True
        assert validator.validate_row(grid, 4, 5) is False


class TestColumnValidation:
    """Test column validation."""

    def test_validate_column_with_no_conflict(self):
        """Test valid column with no conflicts."""
        grid = [
            5, 0, 0, 0, 0, 0, 0, 0, 0,
            3, 0, 0, 0, 0, 0, 0, 0, 0,
            4, 0, 0, 0, 0, 0, 0, 0, 0,
            6, 0, 0, 0, 0, 0, 0, 0, 0,
            7, 0, 0, 0, 0, 0, 0, 0, 0,
            8, 0, 0, 0, 0, 0, 0, 0, 0,
            9, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 0, 0, 0, 0, 0, 0, 0,
            2, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert validator.validate_column(grid, 0, 5) is False  # 5 already in col
        assert validator.validate_column(grid, 0, 9) is False  # 9 already in col
        assert validator.validate_column(grid, 1, 5) is True   # col 1 is empty

    def test_validate_column_with_conflict(self):
        """Test column with value conflict."""
        grid = [
            5, 0, 0, 0, 0, 0, 0, 0, 0,  # 5 in col 0
            3, 0, 0, 0, 0, 0, 0, 0, 0,  # 3 in col 0
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        assert validator.validate_column(grid, 0, 5) is False
        assert validator.validate_column(grid, 0, 3) is False
        assert validator.validate_column(grid, 0, 4) is True


class TestBoxValidation:
    """Test 3x3 box validation."""

    def test_validate_box_top_left(self):
        """Test validation for top-left 3x3 box."""
        grid = [
            5, 3, 0, 0, 0, 0, 0, 0, 0,
            6, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 9, 8, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        # Box 0 contains: 5,3,6,9,8
        assert validator.validate_box(grid, 0, 0, 5) is False
        assert validator.validate_box(grid, 0, 0, 1) is True
        assert validator.validate_box(grid, 1, 1, 3) is False
        assert validator.validate_box(grid, 2, 2, 8) is False

    def test_validate_box_center(self):
        """Test validation for center 3x3 box."""
        grid = [
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 5, 3, 0, 0, 0, 0,
            0, 0, 0, 6, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 9, 8, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        # Box 4 (center) contains: 5,3,6,9,8
        assert validator.validate_box(grid, 3, 3, 5) is False
        assert validator.validate_box(grid, 4, 4, 1) is True
        assert validator.validate_box(grid, 5, 5, 9) is False


class TestCompleteValidation:
    """Test is_valid_move function."""

    def test_valid_move(self):
        """Test completely valid move."""
        grid = [
            5, 3, 0, 0, 7, 0, 0, 0, 0,
            6, 0, 0, 1, 9, 5, 0, 0, 0,
            0, 9, 8, 0, 0, 0, 0, 6, 0,
            8, 0, 0, 0, 6, 0, 0, 0, 3,
            4, 0, 0, 8, 0, 3, 0, 0, 1,
            7, 0, 0, 0, 2, 0, 0, 0, 6,
            0, 6, 0, 0, 0, 0, 2, 8, 0,
            0, 0, 0, 4, 1, 9, 0, 0, 5,
            0, 0, 0, 0, 8, 0, 0, 7, 9,
        ]
        is_valid, error = validator.is_valid_move(grid, 0, 2, 4)
        assert is_valid is True
        assert error == ""

    def test_invalid_move_row_conflict(self):
        """Test move that violates row rule."""
        grid = [0] * 81
        grid[0] = 5
        is_valid, error = validator.is_valid_move(grid, 0, 5, 5)
        assert is_valid is False
        assert "row" in error.lower()

    def test_invalid_move_column_conflict(self):
        """Test move that violates column rule."""
        grid = [0] * 81
        grid[0] = 5
        is_valid, error = validator.is_valid_move(grid, 5, 0, 5)
        assert is_valid is False
        assert "column" in error.lower()

    def test_invalid_move_box_conflict(self):
        """Test move that violates box rule."""
        grid = [0] * 81
        grid[0] = 5
        is_valid, error = validator.is_valid_move(grid, 1, 1, 5)
        assert is_valid is False
        assert "box" in error.lower()


class TestSolutionChecking:
    """Test complete solution validation."""

    def test_valid_complete_solution(self):
        """Test a valid complete Sudoku solution."""
        grid = [
            5, 3, 4, 6, 7, 8, 9, 1, 2,
            6, 7, 2, 1, 9, 5, 3, 4, 8,
            1, 9, 8, 3, 4, 2, 5, 6, 7,
            8, 5, 9, 7, 6, 1, 4, 2, 3,
            4, 2, 6, 8, 5, 3, 7, 9, 1,
            7, 1, 3, 9, 2, 4, 8, 5, 6,
            9, 6, 1, 5, 3, 7, 2, 8, 4,
            2, 8, 7, 4, 1, 9, 6, 3, 5,
            3, 4, 5, 2, 8, 6, 1, 7, 9,
        ]
        assert validator.check_solution(grid) is True

    def test_incomplete_solution(self):
        """Test incomplete solution (has zeros)."""
        grid = [0] * 81
        assert validator.check_solution(grid) is False

    def test_invalid_solution(self):
        """Test solution that violates Sudoku rules."""
        grid = [
            5, 5, 4, 6, 7, 8, 9, 1, 2,  # Two 5s in row 0
            6, 7, 2, 1, 9, 5, 3, 4, 8,
            1, 9, 8, 3, 4, 2, 5, 6, 7,
            8, 5, 9, 7, 6, 1, 4, 2, 3,
            4, 2, 6, 8, 5, 3, 7, 9, 1,
            7, 1, 3, 9, 2, 4, 8, 5, 6,
            9, 6, 1, 5, 3, 7, 2, 8, 4,
            2, 8, 7, 4, 1, 9, 6, 3, 5,
            3, 4, 5, 2, 8, 6, 1, 7, 9,
        ]
        assert validator.check_solution(grid) is False
