# T-003: REST API Implementation

**Task Type**: Implementation
**Priority**: High
**Estimate**: 6 hours
**Sprint**: Sprint 1
**Status**: 📋 PENDING
**User Stories**: S-002, S-003

---

## Description

Implement REST API endpoints using Django REST Framework for puzzle management, moves, validation, and hints.

## Deliverables

- [ ] `serializers.py` with PuzzleSerializer, MoveSerializer
- [ ] `views.py` with PuzzleViewSet
- [ ] Custom actions: move, validate, hint
- [ ] URL router configuration
- [ ] Error handling and validation

## API Endpoints

1. POST /sudoku/api/puzzles/ - Create puzzle
2. GET /sudoku/api/puzzles/ - List puzzles
3. GET /sudoku/api/puzzles/{id}/ - Retrieve puzzle
4. POST /sudoku/api/puzzles/{id}/move/ - Make move
5. POST /sudoku/api/puzzles/{id}/validate/ - Check solution
6. GET /sudoku/api/puzzles/{id}/hint/ - Get hint
7. DELETE /sudoku/api/puzzles/{id}/ - Delete puzzle

## Acceptance Criteria

- All endpoints return correct HTTP status codes
- Request/response formats follow REST conventions
- Solution field hidden from API responses
- Proper error messages for validation failures

## Testing

- [ ] Test create puzzle (all difficulties)
- [ ] Test list puzzles
- [ ] Test retrieve puzzle
- [ ] Test make valid move
- [ ] Test invalid moves (row/column/box violations)
- [ ] Test modify given cell (should fail)
- [ ] Test validate correct solution
- [ ] Test validate incorrect solution
- [ ] Test get hint
- [ ] Test delete puzzle
- [ ] >95% coverage for serializers.py and API views

---

**Closes #TBD** (GitHub issue to be created)
