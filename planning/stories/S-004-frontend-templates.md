# S-004: Frontend Templates and Interface

**Story Type**: User Story
**Priority**: Medium
**Estimate**: 1 day
**Sprint**: Sprint 1
**Status**: 📋 PENDING

---

## User Story

**As a** player
**I want** a web interface to play Sudoku puzzles
**So that** I can play directly in my browser without building a custom frontend

---

## Acceptance Criteria

- [ ] When I visit `/sudoku/`, I see a list of all puzzles with their difficulty and status
- [ ] When I click "New Puzzle", I can select difficulty and create a new puzzle
- [ ] When I click on a puzzle, I see a 9x9 grid with the current state
- [ ] When I click a cell, I can enter a number (1-9) or clear it
- [ ] When I enter an invalid number, I see an error message
- [ ] When I click "Check Solution", I'm told if my solution is correct
- [ ] When I click "Get Hint", I receive a helpful hint
- [ ] The interface is responsive and works on mobile devices (320px+)

---

## Definition of Done

- [ ] Template files created:
  - `base.html` - Base template with common structure
  - `puzzle_list.html` - List all puzzles
  - `puzzle_detail.html` - Display 9x9 grid for playing
- [ ] CSS file (`sudoku.css`) with:
  - 9x9 grid layout with 3x3 box borders
  - Cell styling (given cells vs editable cells)
  - Responsive design (mobile-first)
  - Error/success message styling
  - Button styling
- [ ] JavaScript file (`sudoku.js`) with:
  - Cell input handling
  - AJAX calls to API (create, move, validate, hint)
  - Grid state management
  - Error/success message display
  - CSRF token handling
- [ ] Template view functions:
  - `puzzle_list(request)` - Render list view
  - `puzzle_detail(request, pk)` - Render detail view
- [ ] URL routing for template views
- [ ] Tests for template views (>95% coverage)
- [ ] Responsive design tested (320px, 768px, 1920px)

---

## Template Structure

### base.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sudoku{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'sudoku/sudoku.css' %}">
</head>
<body>
    <header>
        <h1>Sudoku</h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### puzzle_list.html
```html
{% extends "sudoku/base.html" %}

{% block title %}Puzzles | Sudoku{% endblock %}

{% block content %}
<div class="puzzle-list">
    <div class="list-header">
        <h2>All Puzzles</h2>
        <div class="new-puzzle-controls">
            <select id="difficulty-select">
                <option value="easy">Easy</option>
                <option value="medium" selected>Medium</option>
                <option value="hard">Hard</option>
                <option value="expert">Expert</option>
            </select>
            <button id="new-puzzle-btn" class="btn btn-primary">
                New Puzzle
            </button>
        </div>
    </div>

    {% if puzzles %}
    <table class="puzzles-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Difficulty</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for puzzle in puzzles %}
            <tr>
                <td>#{{ puzzle.id }}</td>
                <td>
                    <span class="difficulty difficulty-{{ puzzle.difficulty }}">
                        {{ puzzle.get_difficulty_display }}
                    </span>
                </td>
                <td>
                    <span class="status status-{{ puzzle.status }}">
                        {{ puzzle.get_status_display }}
                    </span>
                </td>
                <td>{{ puzzle.created_at|date:"Y-m-d H:i" }}</td>
                <td>
                    <a href="{% url 'sudoku:puzzle-detail' puzzle.id %}"
                       class="btn btn-small">
                        Play
                    </a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p class="no-puzzles">No puzzles yet. Create your first puzzle!</p>
    {% endif %}

    <div id="message" class="message"></div>
</div>
{% endblock %}

{% block extra_js %}
{% load static %}
<script src="{% static 'sudoku/sudoku.js' %}"></script>
<script>
    Sudoku.csrfToken = '{{ csrf_token }}';
    // Initialize list page
</script>
{% endblock %}
```

### puzzle_detail.html
```html
{% extends "sudoku/base.html" %}

{% block title %}Puzzle #{{ puzzle.id }} | Sudoku{% endblock %}

{% block content %}
<div class="puzzle-container">
    <div class="puzzle-header">
        <a href="{% url 'sudoku:puzzle-list' %}" class="btn btn-secondary">
            ← Back to Puzzles
        </a>
        <h2>
            Puzzle #{{ puzzle.id }}
            <span class="difficulty difficulty-{{ puzzle.difficulty }}">
                {{ puzzle.get_difficulty_display }}
            </span>
        </h2>
    </div>

    <div class="puzzle-info">
        <div class="info-item">
            <span class="label">Status:</span>
            <span id="puzzle-status" class="value status-{{ puzzle.status }}">
                {{ puzzle.get_status_display }}
            </span>
        </div>
    </div>

    <div id="sudoku-grid" class="sudoku-grid" data-puzzle-id="{{ puzzle.id }}">
        {% for cell in puzzle.current_state %}
        <input
            type="text"
            class="cell {% if puzzle.puzzle|index:forloop.counter0 != 0 %}given{% endif %}"
            data-index="{{ forloop.counter0 }}"
            data-row="{{ forloop.counter0|divisibleby:9 }}"
            data-col="{{ forloop.counter0|modulo:9 }}"
            value="{% if cell != 0 %}{{ cell }}{% endif %}"
            maxlength="1"
            pattern="[1-9]"
            {% if puzzle.puzzle|index:forloop.counter0 != 0 %}readonly{% endif %}
        />
        {% endfor %}
    </div>

    <div class="puzzle-actions">
        <button id="check-btn" class="btn btn-primary">Check Solution</button>
        <button id="hint-btn" class="btn btn-secondary">Get Hint</button>
        <button id="new-puzzle-btn" class="btn btn-secondary">New Puzzle</button>
    </div>

    <div id="message" class="message"></div>
</div>
{% endblock %}

{% block extra_js %}
{% load static %}
<script src="{% static 'sudoku/sudoku.js' %}"></script>
<script>
    Sudoku.csrfToken = '{{ csrf_token }}';
    Sudoku.initPuzzle({{ puzzle.id }});
</script>
{% endblock %}
```

---

## CSS Styling (sudoku.css)

### Grid Layout
```css
.sudoku-grid {
    display: grid;
    grid-template-columns: repeat(9, 1fr);
    grid-template-rows: repeat(9, 1fr);
    gap: 0;
    max-width: 540px;
    margin: 2rem auto;
    border: 3px solid #333;
}

.cell {
    width: 60px;
    height: 60px;
    border: 1px solid #ccc;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

/* 3x3 box borders */
.cell:nth-child(9n+3),
.cell:nth-child(9n+6) {
    border-right: 2px solid #333;
}

.cell:nth-child(n+19):nth-child(-n+27),
.cell:nth-child(n+46):nth-child(-n+54) {
    border-bottom: 2px solid #333;
}

/* Given cells (from original puzzle) */
.cell.given {
    background-color: #f0f0f0;
    color: #333;
    font-weight: bold;
}

/* Editable cells */
.cell:not(.given) {
    background-color: white;
    color: #0066cc;
}

.cell:not(.given):focus {
    outline: 2px solid #0066cc;
    background-color: #e6f2ff;
}

/* Error state */
.cell.error {
    background-color: #ffe6e6;
    color: #cc0000;
}
```

### Responsive Design
```css
@media (max-width: 768px) {
    .cell {
        width: 40px;
        height: 40px;
        font-size: 18px;
    }
}

@media (max-width: 480px) {
    .cell {
        width: 30px;
        height: 30px;
        font-size: 14px;
    }
}
```

---

## JavaScript (sudoku.js)

### Core Functionality
```javascript
const Sudoku = {
    apiBaseUrl: '/sudoku/api',
    currentPuzzleId: null,
    csrfToken: null,

    async createPuzzle(difficulty) {
        // POST to /api/puzzles/
    },

    async loadPuzzle(puzzleId) {
        // GET /api/puzzles/{id}/
    },

    async makeMove(puzzleId, row, col, value) {
        // POST /api/puzzles/{id}/move/
    },

    async checkSolution(puzzleId) {
        // POST /api/puzzles/{id}/validate/
    },

    async getHint(puzzleId) {
        // GET /api/puzzles/{id}/hint/
    },

    updateGrid(puzzleData) {
        // Update grid cells with current state
    },

    handleCellInput(event) {
        // Handle cell value changes
    },

    showMessage(text, type) {
        // Display success/error messages
    },

    initPuzzle(puzzleId) {
        // Initialize puzzle detail page
    }
};
```

---

## Visual Design

### Color Scheme
- Primary: #0066cc (blue)
- Success: #28a745 (green)
- Error: #dc3545 (red)
- Warning: #ffc107 (amber)
- Given cells: #f0f0f0 (light gray)
- Grid borders: #333 (dark gray)

### Difficulty Badges
- Easy: Green
- Medium: Blue
- Hard: Orange
- Expert: Red

### Status Badges
- In Progress: Blue
- Solved: Green
- Abandoned: Gray

---

## Tasks

This story is implemented through:
- T-004: Frontend Templates

---

## Test Coverage

### Template View Tests (test_views.py)

- [ ] Test puzzle list view renders
- [ ] Test puzzle list view shows all puzzles
- [ ] Test puzzle detail view renders
- [ ] Test puzzle detail view displays correct grid
- [ ] Test puzzle detail view 404 for non-existent puzzle
- [ ] Test template tags and filters
- [ ] Test responsive design (visual regression)

---

## Accessibility

- [ ] Keyboard navigation works (tab, arrow keys)
- [ ] Screen reader friendly (ARIA labels)
- [ ] High contrast mode support
- [ ] Focus indicators visible
- [ ] Error messages announced

---

## Notes

- Use vanilla JavaScript (no jQuery/React)
- CSRF token must be included in all AJAX requests
- Grid should be touch-friendly on mobile
- Consider number pad on mobile devices
- Auto-save on blur (optional enhancement)
- Mirror successful patterns from django-tictactoe
