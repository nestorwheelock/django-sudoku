"""
API views for Sudoku app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Puzzle
from .serializers import (
    PuzzleSerializer,
    PuzzleCreateSerializer,
    MoveSerializer,
    CheckResponseSerializer,
    HintResponseSerializer,
)


class PuzzleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Sudoku puzzles.

    Endpoints:
    - GET /api/puzzles/ - List all puzzles
    - POST /api/puzzles/ - Create new puzzle
    - GET /api/puzzles/{id}/ - Retrieve specific puzzle
    - DELETE /api/puzzles/{id}/ - Delete puzzle
    - POST /api/puzzles/{id}/move/ - Make a move
    - POST /api/puzzles/{id}/check/ - Check solution
    - POST /api/puzzles/{id}/hint/ - Get hint
    - POST /api/puzzles/{id}/reset/ - Reset puzzle
    """

    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['difficulty', 'status']

    def get_serializer_class(self):
        """Use different serializer for create action."""
        if self.action == 'create':
            return PuzzleCreateSerializer
        return PuzzleSerializer

    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """
        Make a move on the puzzle.

        POST /api/puzzles/{id}/move/
        Body: {"row": 0-8, "col": 0-8, "value": 1-9}

        Returns:
        - 200: Move successful with updated current_state
        - 400: Invalid move with error message
        """
        puzzle = self.get_object()
        serializer = MoveSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        row = serializer.validated_data['row']
        col = serializer.validated_data['col']
        value = serializer.validated_data['value']

        success, message = puzzle.make_move(row, col, value)

        if not success:
            return Response(
                {'success': False, 'message': message},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'success': True,
            'message': message,
            'current_state': puzzle.current_state,
        })

    @action(detail=True, methods=['post'])
    def check(self, request, pk=None):
        """
        Check if puzzle solution is complete and correct.

        POST /api/puzzles/{id}/check/

        Returns:
        - 200: Check result with complete/correct status and errors
        """
        puzzle = self.get_object()
        is_complete, is_correct, errors = puzzle.check_solution()

        return Response({
            'complete': is_complete,
            'correct': is_correct,
            'errors': errors,
        })

    @action(detail=True, methods=['post'])
    def hint(self, request, pk=None):
        """
        Get a hint for the next move.

        POST /api/puzzles/{id}/hint/

        Returns:
        - 200: Hint with row, col, value (or nulls if complete)
        """
        puzzle = self.get_object()
        row, col, value = puzzle.get_hint()

        return Response({
            'row': row,
            'col': col,
            'value': value,
        })

    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        """
        Reset puzzle to initial state.

        POST /api/puzzles/{id}/reset/

        Returns:
        - 200: Success message with reset current_state
        """
        puzzle = self.get_object()
        puzzle.reset()

        return Response({
            'message': 'Puzzle reset to initial state',
            'current_state': puzzle.current_state,
        })


# Template-based views for web interface

from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy


class PuzzleListView(ListView):
    """List all Sudoku puzzles."""
    model = Puzzle
    template_name = 'sudoku/puzzle_list.html'
    context_object_name = 'puzzles'


class PuzzleCreateView(CreateView):
    """Create a new Sudoku puzzle."""
    model = Puzzle
    template_name = 'sudoku/puzzle_create.html'
    fields = ['difficulty']

    def get_success_url(self):
        return reverse_lazy('sudoku:puzzle_play', args=[self.object.id])


class PuzzlePlayView(DetailView):
    """Play a Sudoku puzzle."""
    model = Puzzle
    template_name = 'sudoku/puzzle_play.html'
    context_object_name = 'puzzle'


class PuzzleDeleteView(DeleteView):
    """Delete a Sudoku puzzle."""
    model = Puzzle
    success_url = reverse_lazy('sudoku:puzzle_list')
