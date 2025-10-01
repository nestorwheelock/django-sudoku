# django-sudoku (SPEC Phase - Awaiting Approval)

⚠️ **STATUS**: This project is in SPEC phase. No code has been written yet.
This README guides you through the approval process.

---

## What This Will Be

**django-sudoku** will be a reusable Django app module that provides complete Sudoku puzzle game functionality. Install it via pip, add to INSTALLED_APPS, and get:

- **9x9 Sudoku Puzzles** with 4 difficulty levels (Easy, Medium, Hard, Expert)
- **REST API** for puzzle management (create, play, validate, hints)
- **Web Interface** with responsive 9x9 grid (optional)
- **Complete Validation** enforcing row/column/box rules
- **>95% Test Coverage** with comprehensive test suite

Similar to django-tictactoe, but for Sudoku.

---

## SPEC Documents for Review

Please review these planning documents before approving:

### Core Planning
- **[PROJECT_CHARTER.md](planning/PROJECT_CHARTER.md)** - Complete project definition
  - What/Why/How
  - Success criteria
  - Scope (IN/OUT)
  - Risks and timeline

- **[SPEC_SUMMARY.md](planning/SPEC_SUMMARY.md)** - Quick reference
  - Overview
  - User stories summary
  - Tasks summary
  - Key features

### User Stories (4 total)
- **[S-001: Portable Django App Module](planning/stories/S-001-django-app-module.md)**
  - Pip installable Django app
  - No configuration required

- **[S-002: Sudoku Puzzle Management API](planning/stories/S-002-puzzle-board-api.md)**
  - REST API (7 endpoints)
  - Puzzle CRUD operations
  - Move validation

- **[S-003: Puzzle Validation & Solution Checking](planning/stories/S-003-validation-solution.md)**
  - Sudoku rule enforcement
  - Solution verification
  - Hint system

- **[S-004: Frontend Templates and Interface](planning/stories/S-004-frontend-templates.md)**
  - Web UI with 9x9 grid
  - Responsive design
  - AJAX integration

### Tasks (5 total)
- **[T-001: Django App Module Setup](planning/tasks/T-001-module-setup.md)** - 4 hours
- **[T-002: Puzzle Model & Migrations](planning/tasks/T-002-puzzle-model.md)** - 6 hours
- **[T-003: REST API Implementation](planning/tasks/T-003-rest-api.md)** - 6 hours
- **[T-004: Frontend Templates](planning/tasks/T-004-frontend-templates.md)** - 6 hours
- **[T-005: Package Documentation](planning/tasks/T-005-documentation.md)** - 4 hours

**Total Estimate:** 26 hours (~3-4 days)

---

## Approval Process

### Step 1: Review Documents
Read all SPEC documents listed above. Pay special attention to:
- Scope (what IS and is NOT included)
- User story acceptance criteria
- Technical approach
- Timeline and estimates

### Step 2: Ask Questions
If anything is unclear:
1. Open GitHub Issue #1 (SPEC Approval)
2. Add your questions as comments
3. Developer will clarify and update docs if needed

### Step 3: Approve
Once satisfied with the SPEC:
1. Go to GitHub Issue #1
2. Add comment: "SPEC approved ✅"
3. Close the issue

**Closing Issue #1 = Formal approval to begin BUILD phase**

---

## What Happens After Approval

Once you approve the SPEC:

1. **Scope Locks** - Changes require new approval process
2. **BUILD Phase Begins** - Following 23-step TDD cycle per CLAUDE.md
3. **GitHub Issues Created** - T-001 through T-005 as separate issues
4. **This README Replaced** - With production documentation
5. **Development Follows** - SPEC → BUILD → VALIDATION → ACCEPTANCE TEST → SHIP

**Estimated Timeline:**
- BUILD: 26 hours
- VALIDATION: 1 hour
- ACCEPTANCE TEST: 1 hour (your hands-on testing)
- SHIP: 1 hour
- **Total: ~30 hours** (3-4 days)

---

## Key Features (Planned)

### Core Functionality
- 9x9 Sudoku grid (81 cells, JSON storage)
- Puzzle generation at 4 difficulty levels
- Move validation (row/column/box rules)
- Solution checking
- Hint system

### REST API Endpoints
```
POST   /sudoku/api/puzzles/           Create puzzle
GET    /sudoku/api/puzzles/           List all puzzles
GET    /sudoku/api/puzzles/{id}/      Get puzzle state
POST   /sudoku/api/puzzles/{id}/move/ Make a move
POST   /sudoku/api/puzzles/{id}/validate/ Check solution
GET    /sudoku/api/puzzles/{id}/hint/ Get a hint
DELETE /sudoku/api/puzzles/{id}/      Delete puzzle
```

### Web Interface
- Puzzle list page
- 9x9 interactive grid
- Cell input with validation
- Check solution / Get hint buttons
- Responsive design (mobile-first)

---

## Technology Stack

- **Backend:** Django 4.0+, Python 3.8+
- **API:** Django REST Framework 3.14+
- **Frontend:** Vanilla JavaScript + CSS
- **Testing:** pytest, pytest-django, pytest-cov
- **Package:** Pip installable

---

## Architecture Preview

### Data Model
```python
class Puzzle(models.Model):
    puzzle = JSONField()        # Original (given cells)
    solution = JSONField()      # Complete solution
    current_state = JSONField() # Player progress
    difficulty = CharField()    # easy/medium/hard/expert
    status = CharField()        # in_progress/solved/abandoned
```

### Grid Storage
- 81-element array (0-80 indices)
- Values: 0 = empty, 1-9 = filled
- row = index // 9, col = index % 9

### Validation Rules
1. **Row:** Each row must contain 1-9 exactly once
2. **Column:** Each column must contain 1-9 exactly once
3. **Box:** Each 3x3 box must contain 1-9 exactly once

---

## Success Criteria

The project will be considered successful when:

- ✅ Pip installable Django app
- ✅ Puzzles generate at all 4 difficulties
- ✅ Validation enforces all Sudoku rules
- ✅ REST API fully functional (7 endpoints)
- ✅ Web interface playable
- ✅ >95% test coverage
- ✅ Complete documentation
- ✅ Client (you) approves for production

---

## Scope Boundaries

### ✅ IN SCOPE (v1.0.0)
- 9x9 standard Sudoku
- 4 difficulty levels
- Puzzle generation & validation
- REST API
- Web interface
- Tests & documentation

### ❌ OUT OF SCOPE (Future Versions)
- Multiplayer/competitive mode
- User authentication
- Leaderboards/statistics
- Timer/scoring system
- 4x4 or 16x16 variant grids
- AI solver
- Undo/redo functionality

---

## Questions?

- **GitHub:** Create or comment on Issue #1
- **Email:** [If applicable]
- **Slack/Discord:** [If applicable]

---

## Next Steps

1. ✅ Review all SPEC documents (you are here)
2. ⏳ Ask questions (if needed)
3. ⏳ Approve by closing GitHub Issue #1
4. ⏳ Wait for BUILD phase to begin

---

**Created:** 2025-09-30
**Status:** 📋 AWAITING CLIENT APPROVAL
**GitHub:** https://github.com/nestorwheelock/django-sudoku (to be created)

---

*This README will be replaced with production documentation once BUILD phase begins.*
