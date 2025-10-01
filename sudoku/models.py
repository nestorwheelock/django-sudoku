"""
Sudoku puzzle models.
"""

import random
from django.db import models
from . import generator, validator


class Puzzle(models.Model):
    """
    Sudoku puzzle model.

    Stores puzzle state, solution, and game metadata.
    Grid format: 81-element JSON array (index 0-80), 0=empty, 1-9=filled.
    """

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('expert', 'Expert'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    puzzle = models.JSONField(
        help_text="Initial puzzle state with clues (81-element list)"
    )
    solution = models.JSONField(
        help_text="Complete valid solution (81-element list)"
    )
    current_state = models.JSONField(
        help_text="Current game state with player moves (81-element list)"
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        help_text="Puzzle difficulty level"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Current puzzle status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Puzzle {self.id} - {self.difficulty} - {self.status}"

    def save(self, *args, **kwargs):
        """Override save to generate puzzle if needed."""
        if not self.puzzle or not self.solution:
            # Generate new puzzle
            self.puzzle, self.solution = generator.generate_puzzle(self.difficulty)
            self.current_state = self.puzzle.copy()

        super().save(*args, **kwargs)

    def make_move(self, row: int, col: int, value: int) -> tuple[bool, str]:
        """
        Make a move on the puzzle.

        Args:
            row: Row index (0-8)
            col: Column index (0-8)
            value: Value to place (1-9)

        Returns:
            Tuple of (success, message)
            - (True, "") if move is valid and applied
            - (False, "error message") if move is invalid
        """
        # Validate coordinates
        if not (0 <= row < 9 and 0 <= col < 9):
            return False, "Invalid coordinates. Row and column must be 0-8."

        # Validate value
        if not (1 <= value <= 9):
            return False, "Invalid value. Must be between 1-9."

        idx = row * 9 + col

        # Check if cell is a pre-filled clue
        if self.puzzle[idx] != 0:
            return False, "Cannot change pre-filled clue cells."

        # Check if move is valid according to Sudoku rules
        is_valid, error = validator.is_valid_move(self.current_state, row, col, value)

        if not is_valid:
            return False, error

        # Apply move
        self.current_state[idx] = value
        self.save()

        return True, ""

    def check_solution(self) -> tuple[bool, bool, list]:
        """
        Check if current solution is complete and correct.

        Returns:
            Tuple of (is_complete, is_correct, errors)
            - is_complete: True if no empty cells
            - is_correct: True if solution matches
            - errors: List of error dictionaries with row/col/current/correct
        """
        # Check if complete (no zeros)
        is_complete = 0 not in self.current_state

        if not is_complete:
            return False, False, []

        # Check if correct
        errors = validator.find_errors(self.current_state, self.solution)
        is_correct = len(errors) == 0

        # Update status if completed correctly
        if is_correct:
            self.status = 'completed'
            self.save()

        return is_complete, is_correct, errors

    def get_hint(self) -> tuple:
        """
        Get a hint for the next move.

        Returns:
            Tuple of (row, col, value) for a random empty cell,
            or (None, None, None) if puzzle is complete
        """
        # Find all empty cells
        empty_cells = [i for i in range(81) if self.current_state[i] == 0]

        if not empty_cells:
            return None, None, None

        # Pick random empty cell
        idx = random.choice(empty_cells)
        row = idx // 9
        col = idx % 9
        value = self.solution[idx]

        return row, col, value

    def reset(self):
        """Reset puzzle to initial state."""
        self.current_state = self.puzzle.copy()
        self.status = 'active'
        self.save()
