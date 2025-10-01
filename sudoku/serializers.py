"""
Serializers for Sudoku API.
"""

from rest_framework import serializers
from .models import Puzzle


class PuzzleSerializer(serializers.ModelSerializer):
    """
    Serializer for Puzzle model.

    Excludes 'solution' field to prevent cheating.
    """

    class Meta:
        model = Puzzle
        fields = [
            'id',
            'puzzle',
            'current_state',
            'difficulty',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'puzzle', 'current_state', 'status', 'created_at', 'updated_at']


class PuzzleCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new puzzles.

    Allows specifying difficulty, generates puzzle automatically.
    """

    class Meta:
        model = Puzzle
        fields = ['id', 'difficulty', 'puzzle', 'current_state', 'status', 'created_at']
        read_only_fields = ['id', 'puzzle', 'current_state', 'status', 'created_at']


class MoveSerializer(serializers.Serializer):
    """Serializer for making a move."""

    row = serializers.IntegerField(min_value=0, max_value=8)
    col = serializers.IntegerField(min_value=0, max_value=8)
    value = serializers.IntegerField(min_value=1, max_value=9)


class CheckResponseSerializer(serializers.Serializer):
    """Serializer for check solution response."""

    complete = serializers.BooleanField()
    correct = serializers.BooleanField()
    errors = serializers.ListField(child=serializers.DictField())


class HintResponseSerializer(serializers.Serializer):
    """Serializer for hint response."""

    row = serializers.IntegerField(allow_null=True)
    col = serializers.IntegerField(allow_null=True)
    value = serializers.IntegerField(allow_null=True)
