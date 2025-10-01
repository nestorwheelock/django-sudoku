# S-003: Puzzle Validation & Solution Checking

**Story Type**: User Story
**Priority**: High
**Estimate**: 1 day
**Sprint**: Sprint 1
**Status**: 📋 PENDING

---

## User Story

**As a** player
**I want** the game to validate my moves and check my solution
**So that** I know when I make mistakes and when I've correctly solved the puzzle

---

## Acceptance Criteria

- [ ] When I enter a number that already exists in the same row, I get an error
- [ ] When I enter a number that already exists in the same column, I get an error
- [ ] When I enter a number that already exists in the same 3x3 box, I get an error
- [ ] When I try to modify a given cell (from original puzzle), I get an error
- [ ] When I enter a valid number, it's accepted and the grid updates
- [ ] When I check my solution and it's correct, the puzzle status becomes 'solved'
- [ ] When I check my solution and it's incorrect, I see which cells have errors
- [ ] When the puzzle is complete and correct, I'm notified of success

---

## Definition of Done

- [ ] Validator module (validator.py) with Sudoku rule checking:
  - `validate_row(grid, row, value)` - Check if value exists in row
  - `validate_column(grid, col, value)` - Check if value exists in column
  - `validate_box(grid, row, col, value)` - Check if value exists in 3x3 box
  - `is_valid_move(grid, row, col, value)` - All rules combined
  - `check_solution(grid)` - Verify complete solution
  - `find_errors(grid, solution)` - Identify incorrect cells
- [ ] Model method `make_move()` uses validator before updating grid
- [ ] Model method `check_solution()` compares current_state to solution
- [ ] Model method `is_given_cell()` checks if cell is from original puzzle
- [ ] API endpoint `/validate/` returns detailed error information
- [ ] Comprehensive validation tests (>95% coverage):
  - Row validation (all 9 rows)
  - Column validation (all 9 columns)
  - Box validation (all 9 boxes)
  - Given cell protection
  - Complete solution checking
  - Partial solution with errors
- [ ] Edge cases tested (empty grid, full grid, single error)

---

## Sudoku Validation Rules

### Rule 1: Row Constraint
Each of the 9 rows must contain digits 1-9 exactly once.
```
Row 0: [5, 3, 4, 6, 7, 8, 9, 1, 2]  ✅ Valid (all 1-9 present)
Row 1: [6, 7, 2, 1, 9, 5, 3, 4, 4]  ❌ Invalid (4 appears twice)
```

### Rule 2: Column Constraint
Each of the 9 columns must contain digits 1-9 exactly once.
```
Col 0: [5, 6, 1, 8, 4, 7, 9, 2, 3]  ✅ Valid
Col 1: [3, 7, 9, 5, 2, 1, 6, 8, 3]  ❌ Invalid (3 appears twice)
```

### Rule 3: Box Constraint
Each of the 9 3x3 boxes must contain digits 1-9 exactly once.
```
Box 0 (top-left):
[5, 3, 4]
[6, 7, 2]
[1, 9, 8]  ✅ Valid

Box 4 (center):
[5, 4, 3]
[8, 2, 9]
[6, 1, 5]  ❌ Invalid (5 appears twice)
```

### Box Index Calculation
```
box_row = row // 3
box_col = col // 3
box_index = box_row * 3 + box_col

Box layout:
[0, 1, 2]
[3, 4, 5]
[6, 7, 8]
```

---

## Technical Implementation

### Validator Module

**validator.py:**
```python
from typing import List, Dict, Tuple

def validate_row(grid: List[int], row: int, value: int) -> bool:
    """Check if value already exists in row."""
    start = row * 9
    end = start + 9
    return value not in grid[start:end]

def validate_column(grid: List[int], col: int, value: int) -> bool:
    """Check if value already exists in column."""
    column_values = [grid[i] for i in range(col, 81, 9)]
    return value not in column_values

def validate_box(grid: List[int], row: int, col: int, value: int) -> bool:
    """Check if value already exists in 3x3 box."""
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            index = r * 9 + c
            if grid[index] == value:
                return False
    return True

def is_valid_move(
    grid: List[int],
    row: int,
    col: int,
    value: int
) -> Tuple[bool, str]:
    """
    Validate move against all Sudoku rules.

    Returns:
        (is_valid, error_message)
    """
    if not validate_row(grid, row, value):
        return False, f"Value {value} already exists in row {row}"

    if not validate_column(grid, col, value):
        return False, f"Value {value} already exists in column {col}"

    if not validate_box(grid, row, col, value):
        return False, f"Value {value} already exists in 3x3 box"

    return True, ""

def check_solution(grid: List[int]) -> bool:
    """
    Check if grid is a valid complete Sudoku solution.

    Returns:
        True if valid and complete, False otherwise
    """
    # Check grid is complete (no zeros)
    if 0 in grid:
        return False

    # Validate all rows
    for row in range(9):
        start = row * 9
        row_values = grid[start:start + 9]
        if set(row_values) != set(range(1, 10)):
            return False

    # Validate all columns
    for col in range(9):
        col_values = [grid[i] for i in range(col, 81, 9)]
        if set(col_values) != set(range(1, 10)):
            return False

    # Validate all boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_values = []
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    box_values.append(grid[r * 9 + c])
            if set(box_values) != set(range(1, 10)):
                return False

    return True

def find_errors(
    current: List[int],
    solution: List[int]
) -> List[Dict[str, int]]:
    """
    Find cells that don't match the solution.

    Returns:
        List of {"row": row, "col": col, "current": val, "correct": val}
    """
    errors = []
    for i in range(81):
        if current[i] != 0 and current[i] != solution[i]:
            errors.append({
                "row": i // 9,
                "col": i % 9,
                "current": current[i],
                "correct": solution[i]
            })
    return errors
```

### Model Integration

**models.py:**
```python
from . import validator

def make_move(self, row: int, col: int, value: int) -> dict:
    """Make a move with validation."""
    # Check if cell is given (original puzzle)
    index = row * 9 + col
    if self.puzzle[index] != 0:
        raise ValidationError("Cannot modify given cell")

    # Validate move
    is_valid, error = validator.is_valid_move(
        self.current_state, row, col, value
    )
    if not is_valid:
        raise ValidationError(error)

    # Apply move
    self.current_state[index] = value

    # Check if solved
    if validator.check_solution(self.current_state):
        self.status = 'solved'

    self.save()
    return {"success": True, "message": "Move successful"}

def check_solution(self) -> dict:
    """Check if current solution is correct."""
    is_correct = (self.current_state == self.solution)

    if is_correct:
        self.status = 'solved'
        self.save()
        return {
            "is_correct": True,
            "message": "Congratulations! Puzzle solved correctly."
        }
    else:
        errors = validator.find_errors(self.current_state, self.solution)
        return {
            "is_correct": False,
            "errors": errors,
            "message": f"Found {len(errors)} error(s)"
        }
```

---

## Test Coverage

### Unit Tests (test_validator.py)

- [ ] Test row validation (9 rows, valid and invalid)
- [ ] Test column validation (9 columns, valid and invalid)
- [ ] Test box validation (9 boxes, valid and invalid)
- [ ] Test complete solution checking (valid solutions)
- [ ] Test incomplete solution (contains zeros)
- [ ] Test invalid solution (violates rules)
- [ ] Test error finding (multiple errors)
- [ ] Edge cases (empty grid, single error, all errors)

### Integration Tests (test_models.py)

- [ ] Test make_move with valid move
- [ ] Test make_move with row violation
- [ ] Test make_move with column violation
- [ ] Test make_move with box violation
- [ ] Test make_move on given cell (should fail)
- [ ] Test check_solution with correct solution
- [ ] Test check_solution with incorrect solution
- [ ] Test check_solution with incomplete puzzle

---

## Tasks

This story is implemented through:
- T-002: Puzzle Model & Migrations (includes validator.py)
- T-003: REST API Implementation (validate endpoint)

---

## Notes

- Validation must be fast (<50ms per move)
- Error messages should be clear and helpful
- Given cells (from original puzzle) are immutable
- Solution field should never be exposed via API
- All validation happens server-side (never trust client)
