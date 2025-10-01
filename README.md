# django-sudoku

A reusable Django app module that provides complete Sudoku puzzle game functionality with REST API and web interface.

[![Tests](https://img.shields.io/badge/tests-95%20passing-brightgreen)](https://github.com/nestorwheelock/django-sudoku)
[![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)](https://github.com/nestorwheelock/django-sudoku)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.0%2B-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Features

- **9×9 Sudoku Puzzles** with 4 difficulty levels (Easy, Medium, Hard, Expert)
- **REST API** with 8 endpoints for complete puzzle management
- **Web Interface** with responsive interactive 9×9 grid
- **Complete Validation** enforcing row/column/box Sudoku rules
- **Hint System** for assistance during gameplay
- **Solution Checker** with error highlighting
- **99% Test Coverage** with comprehensive test suite
- **Pip Installable** - add to any Django project in minutes

## Quick Start

### Installation

```bash
pip install django-sudoku
```

### Configuration

Add to your Django project's `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.staticfiles',  # Required for web interface
    'rest_framework',              # Required for API
    'sudoku',                      # django-sudoku
]
```

Add to your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('sudoku/', include('sudoku.urls')),
]
```

Run migrations:

```bash
python manage.py migrate
```

### Usage

#### Web Interface

Visit `http://localhost:8000/sudoku/` to:

- View all your puzzles
- Create new puzzles at different difficulty levels
- Play puzzles with the interactive grid
- Get hints and check solutions

#### REST API

Create a puzzle:

```bash
curl -X POST http://localhost:8000/sudoku/api/puzzles/ \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "medium"}'
```

Make a move:

```bash
curl -X POST http://localhost:8000/sudoku/api/puzzles/1/move/ \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 2, "value": 4}'
```

Check solution:

```bash
curl -X POST http://localhost:8000/sudoku/api/puzzles/1/check/
```

Get a hint:

```bash
curl -X POST http://localhost:8000/sudoku/api/puzzles/1/hint/
```

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/sudoku/api/puzzles/` | Create new puzzle |
| `GET` | `/sudoku/api/puzzles/` | List all puzzles |
| `GET` | `/sudoku/api/puzzles/{id}/` | Get puzzle details |
| `DELETE` | `/sudoku/api/puzzles/{id}/` | Delete puzzle |
| `POST` | `/sudoku/api/puzzles/{id}/move/` | Make a move |
| `POST` | `/sudoku/api/puzzles/{id}/check/` | Check solution |
| `POST` | `/sudoku/api/puzzles/{id}/hint/` | Get hint |
| `POST` | `/sudoku/api/puzzles/{id}/reset/` | Reset to initial state |

### Puzzle Object

```json
{
  "id": 1,
  "puzzle": [5,3,0,0,7,0, ...],
  "current_state": [5,3,4,0,7,0, ...],
  "difficulty": "medium",
  "status": "active",
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:30:00Z"
}
```

**Note**: `solution` field is never exposed via API to prevent cheating.

### Grid Format

Puzzles are stored as 81-element JSON arrays:
- Indices 0-80 represent the 9×9 grid
- Values: `0` = empty, `1-9` = filled
- Calculation: `index = row * 9 + col`

## Difficulty Levels

| Difficulty | Clues | Description |
|------------|-------|-------------|
| Easy | 40-45 | Great for beginners |
| Medium | 30-35 | Moderate challenge |
| Hard | 25-30 | Difficult |
| Expert | 22-25 | Very challenging |

## Development

### Setup Development Environment

```bash
git clone https://github.com/nestorwheelock/django-sudoku.git
cd django-sudoku
pip install -r requirements-dev.txt
```

### Run Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=sudoku --cov-report=term-missing
```

### Test Results

```
95 tests passing
99% code coverage
```

## Architecture

### Models

**Puzzle Model**:
- `puzzle` (JSONField): Original puzzle with clues
- `solution` (JSONField): Complete valid solution
- `current_state` (JSONField): Current player progress
- `difficulty` (CharField): easy/medium/hard/expert
- `status` (CharField): active/completed

### Validation

Three validation rules enforced:

1. **Row Rule**: Each row must contain 1-9 exactly once
2. **Column Rule**: Each column must contain 1-9 exactly once
3. **Box Rule**: Each 3×3 box must contain 1-9 exactly once

### Puzzle Generation

- Uses backtracking algorithm with randomization
- Generates valid complete solution first
- Removes cells based on difficulty level
- Ensures unique solvable puzzles

## Requirements

- Python 3.8+
- Django 4.0+
- djangorestframework 3.14+
- django-filter 23.0+ (for API filtering)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Android)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Roadmap

### v1.0.0 (Current)
- ✅ Core Sudoku functionality
- ✅ REST API
- ✅ Web interface
- ✅ 4 difficulty levels
- ✅ Tests & documentation

### Future Versions
- Multiplayer/competitive mode
- User authentication
- Leaderboards & statistics
- Timer & scoring system
- Undo/redo functionality
- 4×4 and 16×16 variants
- AI solver

## Support

- **Issues**: [GitHub Issues](https://github.com/nestorwheelock/django-sudoku/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nestorwheelock/django-sudoku/discussions)

## Acknowledgments

- Built following AI-Native Development Workflow (CLAUDE.md)
- Inspired by classic Sudoku puzzles
- Similar to django-tictactoe project structure

## Project Stats

- **Version**: 1.0.0
- **Python**: 3.8+
- **Django**: 4.0-5.x
- **Tests**: 95 passing
- **Coverage**: 99%
- **License**: MIT
- **GitHub**: https://github.com/nestorwheelock/django-sudoku

---

**Created**: 2025-09-30
**Status**: ✅ Production Ready
**Maintained by**: Nestor Wheelock

---

*Generated with [Claude Code](https://claude.com/claude-code)*
