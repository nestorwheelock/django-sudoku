"""
Sudoku validation logic.

Provides functions to validate moves and check complete solutions.
Grid format: 81-element list, index 0-80, 0=empty, 1-9=filled.
"""

from typing import List, Tuple, Dict


def validate_row(grid: List[int], row: int, value: int) -> bool:
    """
    Check if value can be placed in the specified row.

    Args:
        grid: 81-element list representing 9x9 Sudoku grid
        row: Row index (0-8)
        value: Value to check (1-9)

    Returns:
        True if value is NOT already in row (valid move)
        False if value already exists in row (invalid move)
    """
    start_idx = row * 9
    end_idx = start_idx + 9
    row_values = grid[start_idx:end_idx]
    return value not in row_values


def validate_column(grid: List[int], col: int, value: int) -> bool:
    """
    Check if value can be placed in the specified column.

    Args:
        grid: 81-element list representing 9x9 Sudoku grid
        col: Column index (0-8)
        value: Value to check (1-9)

    Returns:
        True if value is NOT already in column (valid move)
        False if value already exists in column (invalid move)
    """
    col_values = [grid[col + i * 9] for i in range(9)]
    return value not in col_values


def validate_box(grid: List[int], row: int, col: int, value: int) -> bool:
    """
    Check if value can be placed in the 3x3 box containing (row, col).

    Args:
        grid: 81-element list representing 9x9 Sudoku grid
        row: Row index (0-8)
        col: Column index (0-8)
        value: Value to check (1-9)

    Returns:
        True if value is NOT already in box (valid move)
        False if value already exists in box (invalid move)
    """
    # Find top-left corner of the 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    # Extract values from the 3x3 box
    box_values = []
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            idx = r * 9 + c
            box_values.append(grid[idx])

    return value not in box_values


def is_valid_move(grid: List[int], row: int, col: int, value: int) -> Tuple[bool, str]:
    """
    Check if a move is valid according to all Sudoku rules.

    Args:
        grid: 81-element list representing 9x9 Sudoku grid
        row: Row index (0-8)
        col: Column index (0-8)
        value: Value to place (1-9)

    Returns:
        Tuple of (is_valid, error_message)
        - (True, "") if move is valid
        - (False, "error description") if move violates a rule
    """
    if not validate_row(grid, row, value):
        return False, f"Value {value} already exists in row {row + 1}"

    if not validate_column(grid, col, value):
        return False, f"Value {value} already exists in column {col + 1}"

    if not validate_box(grid, row, col, value):
        return False, f"Value {value} already exists in the 3x3 box"

    return True, ""


def check_solution(grid: List[int]) -> bool:
    """
    Check if a Sudoku grid is a valid complete solution.

    Args:
        grid: 81-element list representing 9x9 Sudoku grid

    Returns:
        True if grid is a valid complete solution
        False if grid is incomplete or violates Sudoku rules
    """
    # Check for zeros (incomplete)
    if 0 in grid:
        return False

    # Check all rows
    for row in range(9):
        start_idx = row * 9
        end_idx = start_idx + 9
        row_values = grid[start_idx:end_idx]
        if sorted(row_values) != list(range(1, 10)):
            return False

    # Check all columns
    for col in range(9):
        col_values = [grid[col + i * 9] for i in range(9)]
        if sorted(col_values) != list(range(1, 10)):
            return False

    # Check all 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_values = []
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    idx = r * 9 + c
                    box_values.append(grid[idx])
            if sorted(box_values) != list(range(1, 10)):
                return False

    return True


def find_errors(current: List[int], solution: List[int]) -> List[Dict[str, int]]:
    """
    Find cells where current state doesn't match solution.

    Args:
        current: 81-element list of current grid state
        solution: 81-element list of correct solution

    Returns:
        List of dictionaries with 'row', 'col', 'current', 'correct' keys
    """
    errors = []
    for idx in range(81):
        if current[idx] != 0 and current[idx] != solution[idx]:
            row = idx // 9
            col = idx % 9
            errors.append({
                'row': row,
                'col': col,
                'current': current[idx],
                'correct': solution[idx]
            })
    return errors
