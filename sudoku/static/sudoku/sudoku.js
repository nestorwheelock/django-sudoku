// Sudoku Game JavaScript

let selectedCell = null;
let currentPuzzleState = [...currentState];

// Initialize the game
document.addEventListener('DOMContentLoaded', function() {
    renderGrid();
    setupEventListeners();
});

// Render the Sudoku grid
function renderGrid() {
    const grid = document.getElementById('sudokuGrid');
    grid.innerHTML = '';

    for (let i = 0; i < 81; i++) {
        const cell = document.createElement('div');
        cell.className = 'sudoku-cell';
        cell.dataset.index = i;

        const value = currentPuzzleState[i];
        if (value !== 0) {
            cell.textContent = value;
        }

        // Mark clue cells
        if (initialPuzzle[i] !== 0) {
            cell.classList.add('clue');
        }

        // Add click handler
        cell.addEventListener('click', () => selectCell(cell, i));

        grid.appendChild(cell);
    }
}

// Select a cell
function selectCell(cell, index) {
    // Can't select clue cells
    if (cell.classList.contains('clue')) {
        return;
    }

    // Remove previous selection
    if (selectedCell) {
        selectedCell.classList.remove('selected');
    }

    // Select new cell
    selectedCell = cell;
    cell.classList.add('selected');
}

// Setup event listeners
function setupEventListeners() {
    // Number pad buttons
    document.querySelectorAll('.num-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const value = parseInt(btn.dataset.value);
            enterNumber(value);
        });
    });

    // Keyboard input
    document.addEventListener('keydown', (e) => {
        if (selectedCell) {
            const key = e.key;
            if (key >= '1' && key <= '9') {
                enterNumber(parseInt(key));
            } else if (key === '0' || key === 'Backspace' || key === 'Delete') {
                enterNumber(0);
            }
        }
    });

    // Control buttons
    document.getElementById('checkBtn').addEventListener('click', checkSolution);
    document.getElementById('hintBtn').addEventListener('click', getHint);
    document.getElementById('resetBtn').addEventListener('click', resetPuzzle);
}

// Enter a number in the selected cell
function enterNumber(value) {
    if (!selectedCell) {
        showMessage('Please select a cell first', 'info');
        return;
    }

    const index = parseInt(selectedCell.dataset.index);
    const row = Math.floor(index / 9);
    const col = index % 9;

    // Make API call to validate and save move
    if (value === 0) {
        // Clear cell (no API call needed, just update locally)
        currentPuzzleState[index] = 0;
        selectedCell.textContent = '';
        selectedCell.classList.remove('error');
        return;
    }

    fetch(`/api/puzzles/${puzzleId}/move/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ row, col, value })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentPuzzleState = data.current_state;
            selectedCell.textContent = value;
            selectedCell.classList.remove('error');
            hideMessage();
        } else {
            showMessage(data.message, 'error');
            selectedCell.classList.add('error');
        }
    })
    .catch(error => {
        showMessage('Error making move: ' + error, 'error');
    });
}

// Check the solution
function checkSolution() {
    fetch(`/api/puzzles/${puzzleId}/check/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.complete && data.correct) {
            showMessage('🎉 Congratulations! You solved the puzzle correctly!', 'success');
        } else if (data.complete && !data.correct) {
            showMessage('❌ Puzzle is complete but has errors. Keep trying!', 'error');
            highlightErrors(data.errors);
        } else {
            const filled = currentPuzzleState.filter(v => v !== 0).length;
            showMessage(`Puzzle is not complete yet. ${filled}/81 cells filled.`, 'info');
        }
    })
    .catch(error => {
        showMessage('Error checking solution: ' + error, 'error');
    });
}

// Get a hint
function getHint() {
    fetch(`/api/puzzles/${puzzleId}/hint/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.row !== null) {
            const index = data.row * 9 + data.col;
            const cell = document.querySelector(`.sudoku-cell[data-index="${index}"]`);

            // Highlight hint cell
            cell.style.animation = 'pulse 1s ease-in-out 3';
            showMessage(`Hint: Row ${data.row + 1}, Column ${data.col + 1} should be ${data.value}`, 'info');

            // Auto-fill if cell is selected
            if (selectedCell && parseInt(selectedCell.dataset.index) === index) {
                enterNumber(data.value);
            }
        } else {
            showMessage('No hints available - puzzle is complete!', 'info');
        }
    })
    .catch(error => {
        showMessage('Error getting hint: ' + error, 'error');
    });
}

// Reset the puzzle
function resetPuzzle() {
    if (!confirm('Are you sure you want to reset the puzzle? All progress will be lost.')) {
        return;
    }

    fetch(`/api/puzzles/${puzzleId}/reset/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        currentPuzzleState = data.current_state;
        renderGrid();
        selectedCell = null;
        showMessage('Puzzle has been reset', 'info');
    })
    .catch(error => {
        showMessage('Error resetting puzzle: ' + error, 'error');
    });
}

// Highlight error cells
function highlightErrors(errors) {
    errors.forEach(error => {
        const index = error.row * 9 + error.col;
        const cell = document.querySelector(`.sudoku-cell[data-index="${index}"]`);
        cell.classList.add('error');
    });
}

// Show message
function showMessage(text, type) {
    const msgDiv = document.getElementById('message');
    msgDiv.textContent = text;
    msgDiv.className = `message ${type}`;
}

// Hide message
function hideMessage() {
    const msgDiv = document.getElementById('message');
    msgDiv.className = 'message';
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); background-color: #f39c12; }
    }
`;
document.head.appendChild(style);
