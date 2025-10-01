# ACCEPTANCE TEST PLAN
## django-sudoku v1.0.0

**Project**: django-sudoku
**Version**: 1.0.0
**Date**: 2025-09-30
**Phase**: ACCEPTANCE TEST (Client Validation)
**GitHub**: https://github.com/nestorwheelock/django-sudoku

---

## Purpose

This document guides you through hands-on testing of django-sudoku to verify that the implementation meets all requirements from the SPEC phase before shipping to production.

**⚠️ IMPORTANT**: This is CLIENT APPROVAL GATE #2. Your sign-off is required before we can ship to production.

---

## Test Environment Setup

### Prerequisites
- Python 3.8+
- Git

### Installation Steps

```bash
# 1. Clone repository
git clone https://github.com/nestorwheelock/django-sudoku.git
cd django-sudoku

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements-dev.txt

# 4. Apply migrations
DJANGO_SETTINGS_MODULE=tests.settings python manage.py migrate

# 5. Start development server
cd tests
python -m django runserver --settings=settings
```

**Access Application**: http://localhost:8000/sudoku/

---

## User Story Acceptance Tests

### ✅ S-001: Portable Django App Module

**Acceptance Criteria:**
1. Package can be imported without errors
2. App can be added to INSTALLED_APPS
3. Migrations run successfully
4. No configuration required beyond INSTALLED_APPS

**Test Steps:**

```bash
# Test 1: Package import
python3 -c "import sudoku; print(f'✅ sudoku v{sudoku.__version__} imported')"

# Test 2: Verify app configuration
python3 -c "from django.apps import apps; import django; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings'); django.setup(); app = apps.get_app_config('sudoku'); print(f'✅ {app.verbose_name} loaded')"

# Test 3: Run migrations
DJANGO_SETTINGS_MODULE=tests.settings python manage.py migrate --run-syncdb
# Expected: ✅ All migrations applied successfully

# Test 4: Run automated tests
pytest sudoku/tests/test_setup.py -v
# Expected: ✅ 11/11 tests passing
```

**Pass Criteria**: All 4 tests complete without errors

---

### ✅ S-002: Sudoku Puzzle Management API

**Acceptance Criteria:**
1. Can create puzzles via API
2. Can list all puzzles
3. Can retrieve specific puzzle
4. Can make moves via API
5. Can delete puzzles
6. Solution field is never exposed
7. All 4 difficulty levels work

**Test Steps:**

**Test Server Must Be Running**: `python manage.py runserver --settings=tests.settings`

```bash
# Test 1: Create puzzle (easy)
curl -X POST http://localhost:8000/sudoku/api/puzzles/ \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "easy"}' | jq
# Expected: Returns puzzle object with 40-45 clues (non-zero values)

# Test 2: Create puzzle (medium)
curl -X POST http://localhost:8000/sudoku/api/puzzles/ \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "medium"}' | jq
# Expected: Returns puzzle object with 30-35 clues

# Test 3: Create puzzle (hard)
curl -X POST http://localhost:8000/sudoku/api/puzzles/ \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "hard"}' | jq
# Expected: Returns puzzle object with 25-30 clues

# Test 4: Create puzzle (expert)
curl -X POST http://localhost:8000/sudoku/api/puzzles/ \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "expert"}' | jq
# Expected: Returns puzzle object with 22-25 clues

# Test 5: List all puzzles
curl http://localhost:8000/sudoku/api/puzzles/ | jq
# Expected: Array of 4 puzzles, NO 'solution' field visible

# Test 6: Get specific puzzle
curl http://localhost:8000/sudoku/api/puzzles/1/ | jq
# Expected: Puzzle object, NO 'solution' field visible

# Test 7: Make a valid move
curl -X POST http://localhost:8000/sudoku/api/puzzles/1/move/ \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 2, "value": 4}' | jq
# Expected: {"success": true, "message": "", "current_state": [...]}

# Test 8: Make invalid move (duplicate in row)
curl -X POST http://localhost:8000/sudoku/api/puzzles/1/move/ \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 3, "value": 4}' | jq
# Expected: {"success": false, "message": "Value 4 already exists in row 1"}

# Test 9: Delete puzzle
curl -X DELETE http://localhost:8000/sudoku/api/puzzles/1/
# Expected: HTTP 204 No Content

# Test 10: Verify deletion
curl http://localhost:8000/sudoku/api/puzzles/1/ | jq
# Expected: HTTP 404 Not Found
```

**Pass Criteria**: All API endpoints work as expected, solution never exposed

---

### ✅ S-003: Puzzle Validation & Solution Checking

**Acceptance Criteria:**
1. Row rule enforced (no duplicates in row)
2. Column rule enforced (no duplicates in column)
3. Box rule enforced (no duplicates in 3×3 box)
4. Hint system provides valid suggestions
5. Solution checker identifies errors
6. Reset functionality works

**Test Steps:**

```bash
# Test 1: Create new puzzle for testing
curl -X POST http://localhost:8000/sudoku/api/puzzles/ \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "easy"}' | jq '.id'
# Note the puzzle ID (e.g., 5)

# Test 2: Get a hint
curl -X POST http://localhost:8000/sudoku/api/puzzles/5/hint/ | jq
# Expected: {"row": X, "col": Y, "value": Z} with valid coordinates

# Test 3: Check incomplete solution
curl -X POST http://localhost:8000/sudoku/api/puzzles/5/check/ | jq
# Expected: {"complete": false, "correct": false, "errors": []}

# Test 4: Reset puzzle
curl -X POST http://localhost:8000/sudoku/api/puzzles/5/reset/ | jq
# Expected: {"message": "Puzzle reset to initial state", "current_state": [...]}

# Test 5: Run validation tests
pytest sudoku/tests/test_validator.py -v
# Expected: ✅ 14/14 validation tests passing
```

**Pass Criteria**: All validation rules enforced, hint system works

---

### ✅ S-004: Frontend Templates and Interface

**Acceptance Criteria:**
1. Puzzle list page displays all puzzles
2. Can create new puzzle via web form
3. Interactive 9×9 grid renders correctly
4. Can input values via click or keyboard
5. Real-time move validation works
6. Hint button provides assistance
7. Check solution button works
8. Reset button restores initial state
9. Responsive design works on mobile

**Test Steps:**

**Manual Testing** (requires browser):

1. **Puzzle List Page**
   - Navigate to: http://localhost:8000/sudoku/
   - Verify: Table showing all puzzles with difficulty/status/actions
   - Click "New Puzzle" → Should navigate to create form

2. **Create Puzzle**
   - URL: http://localhost:8000/sudoku/create/
   - Select difficulty: Medium
   - Click "Create Puzzle"
   - Verify: Redirects to play page with 9×9 grid

3. **Interactive Grid**
   - Verify: 9×9 grid displayed with thick borders for 3×3 boxes
   - Verify: Clue cells have different background color
   - Click empty cell → Should highlight (blue background)
   - Click clue cell → Should NOT allow selection

4. **Input Methods**
   - **Mouse**: Click cell, then click number button (1-9)
   - **Keyboard**: Click cell, press number key (1-9)
   - Verify: Both methods work

5. **Move Validation**
   - Try entering duplicate number in same row
   - Verify: Error message appears, cell turns red
   - Enter valid number
   - Verify: Number appears in grid, no error

6. **Hint System**
   - Click "Get Hint" button
   - Verify: Message shows "Hint: Row X, Column Y should be Z"
   - Verify: Hint cell briefly pulses/highlights

7. **Solution Checker**
   - Fill some cells (don't complete)
   - Click "Check Solution"
   - Verify: Shows "Puzzle is not complete yet. X/81 cells filled."

8. **Reset Functionality**
   - Make several moves
   - Click "Reset" button
   - Confirm the dialog
   - Verify: Grid returns to initial state (only clues remain)

9. **Responsive Design** (optional)
   - Resize browser window to mobile size (375px width)
   - Verify: Grid scales appropriately
   - Verify: Buttons stack vertically
   - Verify: Still playable on small screen

**Automated Frontend Tests**:

```bash
pytest sudoku/tests/test_views.py -v
# Expected: ✅ 11/11 view tests passing
```

**Pass Criteria**: Web interface fully functional and user-friendly

---

## Complete Solution Test (End-to-End)

**Objective**: Play a complete Sudoku game from creation to solution

**Steps:**

1. **Create Easy Puzzle**
   - Visit: http://localhost:8000/sudoku/create/
   - Select: Easy
   - Click: Create Puzzle

2. **Use Hints to Solve**
   - Click "Get Hint" → Note row, col, value
   - Click the suggested cell
   - Enter the suggested value
   - Repeat 81 times (or use multiple hints strategically)

   **Shortcut**: Use this Python script to auto-solve via API:

   ```python
   import requests
   puzzle_id = 1  # Your puzzle ID
   base_url = f"http://localhost:8000/sudoku/api/puzzles/{puzzle_id}"

   # Get hints and auto-fill until complete
   for _ in range(81):
       hint = requests.post(f"{base_url}/hint/").json()
       if hint['row'] is None:
           break
       move = {
           'row': hint['row'],
           'col': hint['col'],
           'value': hint['value']
       }
       response = requests.post(f"{base_url}/move/", json=move)
       print(f"Filled ({hint['row']},{hint['col']}) = {hint['value']}")

   # Check solution
   result = requests.post(f"{base_url}/check/").json()
   print(f"Complete: {result['complete']}, Correct: {result['correct']}")
   ```

3. **Verify Completion**
   - Click "Check Solution"
   - Verify: "🎉 Congratulations! You solved the puzzle correctly!"
   - Verify: Puzzle status changes to "Completed"

**Pass Criteria**: Can complete full Sudoku game successfully

---

## Performance & Quality Tests

```bash
# Test 1: Full test suite
pytest sudoku/tests/ -v
# Expected: ✅ 95/95 tests passing

# Test 2: Code coverage
pytest --cov=sudoku --cov-report=term
# Expected: ✅ 99% coverage

# Test 3: Puzzle generation speed
python3 -c "
import time
from sudoku import generator

start = time.time()
for difficulty in ['easy', 'medium', 'hard', 'expert']:
    for _ in range(5):
        generator.generate_puzzle(difficulty)
elapsed = time.time() - start
print(f'✅ Generated 20 puzzles in {elapsed:.2f}s ({elapsed/20:.3f}s per puzzle)')
"
# Expected: < 1 second per puzzle
```

**Pass Criteria**: All tests pass, reasonable performance

---

## Known Issues & Limitations

### Documented Limitations (Acceptable)
- ❌ No undo/redo functionality (out of scope v1.0)
- ❌ No timer/scoring system (out of scope v1.0)
- ❌ No user authentication (out of scope v1.0)
- ❌ No multiplayer mode (out of scope v1.0)
- ❌ Solution field intentionally hidden from API (security feature)

### Issues Found During Testing
*(To be filled in by tester)*

| Issue # | Severity | Description | Reproducible? |
|---------|----------|-------------|---------------|
| | | | |

**Severity Levels:**
- **CRITICAL**: Blocks basic functionality, must fix before ship
- **MAJOR**: Significant issue, should fix before ship
- **MINOR**: Small issue, can fix in next version
- **ENHANCEMENT**: New feature request, future version

---

## Acceptance Decision

### Test Results Summary

| User Story | Pass/Fail | Notes |
|------------|-----------|-------|
| S-001: Django App Module | ⏳ PENDING | |
| S-002: API Management | ⏳ PENDING | |
| S-003: Validation | ⏳ PENDING | |
| S-004: Frontend | ⏳ PENDING | |
| Complete Solution Test | ⏳ PENDING | |

### Quality Assessment

| Criteria | Acceptable? | Notes |
|----------|-------------|-------|
| Performance | ⏳ PENDING | |
| Usability | ⏳ PENDING | |
| Reliability | ⏳ PENDING | |
| Documentation | ⏳ PENDING | |

### Issues Summary

- **CRITICAL Issues**: 0
- **MAJOR Issues**: 0
- **MINOR Issues**: 0
- **ENHANCEMENTS**: 0

---

## Client Sign-Off

**Decision** (select one):

- [ ] ✅ **APPROVED FOR PRODUCTION** - Ship immediately as-is
- [ ] ✅ **APPROVED WITH KNOWN ISSUES** - Ship with documented limitations
- [ ] ⚠️ **CONDITIONAL APPROVAL** - Fix critical issues, then ship (no re-test needed)
- [ ] 🔧 **FIX AND RE-TEST** - Fix issues and schedule new acceptance test
- [ ] ❌ **REJECTED** - Major rework needed, return to BUILD/SPEC

**Client Name**: ___________________________

**Client Signature**: ___________________________

**Date**: ___________________________

**Client Notes/Feedback**:
```
[Space for feedback]
```

---

## Next Steps After Approval

### If APPROVED:
1. ✅ Close this acceptance test issue
2. ✅ Proceed to SHIP phase
3. ✅ Tag release v1.0.0
4. ✅ Publish to PyPI (if applicable)
5. ✅ Update project status to "Production Ready"

### If CONDITIONAL/FIX & RE-TEST:
1. 🔧 Create GitHub issues for each problem found
2. 🔧 Return to BUILD phase
3. 🔧 Fix issues
4. 🔧 Re-run VALIDATION phase
5. 🔧 Schedule new ACCEPTANCE TEST

### If REJECTED:
1. ❌ Detailed discussion with client
2. ❌ Determine root cause of rejection
3. ❌ May need to return to SPEC phase
4. ❌ Revise approach and timeline

---

## Pricing Reminder

**Original Estimate**: 33 hours @ $50/hour = $1,650
**AI Efficiency Discount**: 85%
**Client Price**: $247.50

**Actual Development Time**: ~2 hours AI execution time
**Client Savings**: $1,402.50 (85% discount)

---

**Prepared by**: AI Developer (Claude Code)
**Date**: 2025-09-30
**Phase**: ACCEPTANCE TEST
**Status**: ⏳ AWAITING CLIENT TESTING

---

*This acceptance test ensures django-sudoku v1.0.0 meets all requirements before production deployment.*
