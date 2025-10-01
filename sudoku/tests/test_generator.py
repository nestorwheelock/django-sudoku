"""
Tests for Sudoku puzzle generation.
"""

import pytest
from sudoku import generator, validator


class TestSolutionGeneration:
    """Test complete solution generation."""

    def test_generate_solution_creates_valid_grid(self):
        """Test that generated solution is valid."""
        solution = generator.generate_solution()
        assert len(solution) == 81
        assert validator.check_solution(solution) is True

    def test_generate_solution_has_no_zeros(self):
        """Test that solution has no empty cells."""
        solution = generator.generate_solution()
        assert 0 not in solution

    def test_generate_solution_is_random(self):
        """Test that generator produces different solutions."""
        solution1 = generator.generate_solution()
        solution2 = generator.generate_solution()
        # While theoretically possible to be same, extremely unlikely
        assert solution1 != solution2


class TestPuzzleGeneration:
    """Test puzzle generation from solution."""

    def test_generate_puzzle_easy(self):
        """Test easy puzzle generation (40-45 clues)."""
        puzzle, solution = generator.generate_puzzle(difficulty="easy")

        # Check structure
        assert len(puzzle) == 81
        assert len(solution) == 81

        # Check solution is valid
        assert validator.check_solution(solution) is True

        # Check clue count (40-45 for easy)
        clue_count = sum(1 for cell in puzzle if cell != 0)
        assert 40 <= clue_count <= 45

    def test_generate_puzzle_medium(self):
        """Test medium puzzle generation (30-35 clues)."""
        puzzle, solution = generator.generate_puzzle(difficulty="medium")

        assert len(puzzle) == 81
        assert validator.check_solution(solution) is True

        clue_count = sum(1 for cell in puzzle if cell != 0)
        assert 30 <= clue_count <= 35

    def test_generate_puzzle_hard(self):
        """Test hard puzzle generation (25-30 clues)."""
        puzzle, solution = generator.generate_puzzle(difficulty="hard")

        assert len(puzzle) == 81
        assert validator.check_solution(solution) is True

        clue_count = sum(1 for cell in puzzle if cell != 0)
        assert 25 <= clue_count <= 30

    def test_generate_puzzle_expert(self):
        """Test expert puzzle generation (22-25 clues)."""
        puzzle, solution = generator.generate_puzzle(difficulty="expert")

        assert len(puzzle) == 81
        assert validator.check_solution(solution) is True

        clue_count = sum(1 for cell in puzzle if cell != 0)
        assert 22 <= clue_count <= 25

    def test_generate_puzzle_invalid_difficulty(self):
        """Test that invalid difficulty raises error."""
        with pytest.raises(ValueError) as exc_info:
            generator.generate_puzzle(difficulty="impossible")
        assert "difficulty" in str(exc_info.value).lower()

    def test_generate_puzzle_clues_match_solution(self):
        """Test that all clues in puzzle match the solution."""
        puzzle, solution = generator.generate_puzzle(difficulty="medium")

        for idx in range(81):
            if puzzle[idx] != 0:
                assert puzzle[idx] == solution[idx]

    def test_generate_puzzle_default_difficulty(self):
        """Test that default difficulty is medium."""
        puzzle, solution = generator.generate_puzzle()

        clue_count = sum(1 for cell in puzzle if cell != 0)
        # Default should be medium (30-35 clues)
        assert 30 <= clue_count <= 35


class TestHelperFunctions:
    """Test helper functions used in generation."""

    def test_is_valid_solution(self):
        """Test solution validation helper."""
        valid_solution = [
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
        assert generator._is_valid_solution(valid_solution) is True

    def test_is_valid_solution_with_zeros(self):
        """Test that incomplete grids are not valid solutions."""
        incomplete = [0] * 81
        assert generator._is_valid_solution(incomplete) is False
