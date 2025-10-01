"""
Sudoku puzzle generation.

Provides functions to generate valid Sudoku puzzles at different difficulty levels.
"""

import random
from typing import List, Tuple
from . import validator


# Difficulty settings: (min_clues, max_clues)
DIFFICULTY_SETTINGS = {
    'easy': (40, 45),
    'medium': (30, 35),
    'hard': (25, 30),
    'expert': (22, 25),
}


def generate_solution() -> List[int]:
    """
    Generate a complete valid Sudoku solution.

    Uses backtracking algorithm with randomization to create
    a fully solved 9x9 Sudoku grid.

    Returns:
        81-element list representing valid complete solution
    """
    grid = [0] * 81

    def solve(grid: List[int]) -> bool:
        """Recursive backtracking solver with randomization."""
        # Find next empty cell
        for idx in range(81):
            if grid[idx] == 0:
                row = idx // 9
                col = idx % 9

                # Try numbers in random order for variety
                numbers = list(range(1, 10))
                random.shuffle(numbers)

                for num in numbers:
                    if validator.validate_row(grid, row, num) and \
                       validator.validate_column(grid, col, num) and \
                       validator.validate_box(grid, row, col, num):
                        grid[idx] = num

                        if solve(grid):
                            return True

                        grid[idx] = 0

                return False

        return True

    solve(grid)
    return grid


def generate_puzzle(difficulty: str = "medium") -> Tuple[List[int], List[int]]:
    """
    Generate a Sudoku puzzle at specified difficulty level.

    Args:
        difficulty: One of 'easy', 'medium', 'hard', 'expert'

    Returns:
        Tuple of (puzzle, solution) where:
        - puzzle: 81-element list with some cells as 0 (clues removed)
        - solution: 81-element list with complete valid solution

    Raises:
        ValueError: If difficulty is not recognized
    """
    if difficulty not in DIFFICULTY_SETTINGS:
        raise ValueError(
            f"Invalid difficulty '{difficulty}'. "
            f"Must be one of: {', '.join(DIFFICULTY_SETTINGS.keys())}"
        )

    # Generate complete solution
    solution = generate_solution()

    # Create puzzle by removing clues
    min_clues, max_clues = DIFFICULTY_SETTINGS[difficulty]
    target_clues = random.randint(min_clues, max_clues)

    # Start with complete solution
    puzzle = solution.copy()

    # Calculate how many cells to remove
    cells_to_remove = 81 - target_clues

    # Get list of all cell indices and shuffle
    indices = list(range(81))
    random.shuffle(indices)

    # Remove cells
    for idx in indices[:cells_to_remove]:
        puzzle[idx] = 0

    return puzzle, solution


def _is_valid_solution(grid: List[int]) -> bool:
    """
    Check if grid is a valid complete solution.

    This is a helper function that wraps validator.check_solution()
    for use in generator module.

    Args:
        grid: 81-element list representing Sudoku grid

    Returns:
        True if grid is valid complete solution, False otherwise
    """
    return validator.check_solution(grid)
