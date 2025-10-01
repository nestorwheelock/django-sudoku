# S-002: Sudoku Puzzle Management API

**Story Type**: User Story
**Priority**: High
**Estimate**: 2 days
**Sprint**: Sprint 1
**Status**: 📋 PENDING

---

## User Story

**As a** developer using the module
**I want** REST API endpoints for Sudoku puzzle management
**So that** I can integrate Sudoku puzzles into my frontend or application

---

## Acceptance Criteria

- [ ] When I POST to `/api/puzzles/` with difficulty, a new puzzle is created and I receive a puzzle ID
- [ ] When I GET `/api/puzzles/{id}/`, I see the current puzzle state (grid, difficulty, status)
- [ ] When I POST to `/api/puzzles/{id}/move/` with row, col, value, the grid updates
- [ ] When I POST an invalid move (violates Sudoku rules), I receive a 400 error with clear message
- [ ] When I POST to `/api/puzzles/{id}/validate/`, I get response if solution is correct
- [ ] When I GET `/api/puzzles/{id}/hint/`, I receive a valid hint (row, col, value)
- [ ] API responses follow REST conventions and include proper HTTP status codes

---

## Definition of Done

- [ ] Puzzle model created with fields:
  - `puzzle`: JSONField storing 81-cell array (9x9 grid)
  - `solution`: JSONField with complete solution
  - `current_state`: JSONField with player progress
  - `difficulty`: CharField ('easy', 'medium', 'hard', 'expert')
  - `status`: CharField ('in_progress', 'solved', 'abandoned')
  - `created_at`, `updated_at`: DateTimeField
- [ ] PuzzleSerializer with proper field validation
- [ ] PuzzleViewSet with actions: create, retrieve, list, move, validate, hint
- [ ] URL routing configured with namespace 'sudoku'
- [ ] Comprehensive API tests (>95% coverage):
  - Create puzzle (all difficulty levels)
  - Retrieve puzzle
  - Valid moves
  - Invalid moves (violates row/column/box rules)
  - Solution validation
  - Hint generation
  - Edge cases
- [ ] API documentation in README

---

## API Specification

### Endpoints

**Create Puzzle**
```
POST /sudoku/api/puzzles/
{
  "difficulty": "medium"
}

Response 201:
{
  "id": 1,
  "puzzle": [5, 3, 0, 0, 7, ...],  # 81 integers (0-9)
  "current_state": [5, 3, 0, 0, 7, ...],
  "solution": [5, 3, 4, 6, 7, ...],  # Hidden from API
  "difficulty": "medium",
  "status": "in_progress",
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:00:00Z"
}
```

**Get Puzzle State**
```
GET /sudoku/api/puzzles/{id}/

Response 200:
{
  "id": 1,
  "puzzle": [5, 3, 0, 0, 7, ...],
  "current_state": [5, 3, 4, 0, 7, ...],
  "difficulty": "medium",
  "status": "in_progress",
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:05:00Z"
}
```

**Make Move**
```
POST /sudoku/api/puzzles/{id}/move/
{
  "row": 0,
  "col": 2,
  "value": 4
}

Response 200:
{
  "id": 1,
  "current_state": [5, 3, 4, 0, 7, ...],
  "status": "in_progress",
  "message": "Move successful"
}

Response 400 (invalid move):
{
  "error": "Value 4 already exists in row 0"
}

Response 400 (violates column):
{
  "error": "Value 4 already exists in column 2"
}

Response 400 (violates box):
{
  "error": "Value 4 already exists in 3x3 box"
}

Response 400 (given cell):
{
  "error": "Cannot modify given cell"
}
```

**Validate Solution**
```
POST /sudoku/api/puzzles/{id}/validate/

Response 200:
{
  "is_correct": true,
  "status": "solved",
  "message": "Congratulations! Puzzle solved correctly."
}

Response 200 (incorrect):
{
  "is_correct": false,
  "errors": [
    {"row": 3, "col": 5, "error": "Violates box rule"},
    {"row": 7, "col": 2, "error": "Violates column rule"}
  ]
}
```

**Get Hint**
```
GET /sudoku/api/puzzles/{id}/hint/

Response 200:
{
  "row": 0,
  "col": 3,
  "value": 6,
  "message": "Try placing 6 at row 0, column 3"
}

Response 400 (puzzle solved):
{
  "error": "Puzzle is already solved"
}
```

**List Puzzles**
```
GET /sudoku/api/puzzles/

Response 200:
[
  {
    "id": 1,
    "difficulty": "medium",
    "status": "solved",
    ...
  },
  {
    "id": 2,
    "difficulty": "hard",
    "status": "in_progress",
    ...
  }
]
```

**Delete Puzzle**
```
DELETE /sudoku/api/puzzles/{id}/

Response 204 No Content
```

---

## Grid Representation

Grid is stored as JSON array with 81 elements (index 0-80):
```
Index:  0  1  2  3  4  5  6  7  8
Row 0: [5, 3, 0, 0, 7, 0, 0, 0, 0]  # Indices 0-8
Row 1: [6, 0, 0, 1, 9, 5, 0, 0, 0]  # Indices 9-17
Row 2: [0, 9, 8, 0, 0, 0, 0, 6, 0]  # Indices 18-26
Row 3: [8, 0, 0, 0, 6, 0, 0, 0, 3]  # Indices 27-35
Row 4: [4, 0, 0, 8, 0, 3, 0, 0, 1]  # Indices 36-44
Row 5: [7, 0, 0, 0, 2, 0, 0, 0, 6]  # Indices 45-53
Row 6: [0, 6, 0, 0, 0, 0, 2, 8, 0]  # Indices 54-62
Row 7: [0, 0, 0, 4, 1, 9, 0, 0, 5]  # Indices 63-71
Row 8: [0, 0, 0, 0, 8, 0, 0, 7, 9]  # Indices 72-80

Values: 0 (empty), 1-9 (filled)

Convert index to row/col:
row = index // 9
col = index % 9

Convert row/col to index:
index = row * 9 + col
```

---

## Technical Notes

**Model Design**:
- Use JSONField for puzzle storage (portable across DB backends)
- Store original puzzle (given cells), solution, and current state separately
- Status choices as constants
- Add model methods: `make_move()`, `validate_cell()`, `check_solution()`, `get_hint()`

**Validation**:
- Row/col must be 0-8
- Value must be 1-9
- Cannot modify given cells (from original puzzle)
- Must not violate row/column/box rules

**DRF Configuration**:
- Use ModelViewSet for standard CRUD
- Add custom actions for move, validate, hint
- Use serializer validation for move logic
- Hide solution field from API responses (security)

---

## Tasks

This story is implemented through:
- T-002: Puzzle Model & Migrations
- T-003: REST API Implementation

---

## Test Scenarios

1. Create puzzles at all 4 difficulty levels
2. Make valid moves
3. Attempt move that violates row rule
4. Attempt move that violates column rule
5. Attempt move that violates box rule
6. Attempt to modify given cell
7. Validate correct solution
8. Validate incorrect solution with errors
9. Get hints for incomplete puzzle
10. List all puzzles
11. Retrieve non-existent puzzle (404)
12. Delete puzzle
