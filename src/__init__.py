"""
MCQ TUI Package
A Rich-based TUI for answering multiple choice questions from YAML files.
"""

from .question import Question
from .parser import parse_yaml_questions
from .display import display_question, show_result, show_summary
from .input_handlers import get_user_answer

__all__ = [
    'Question',
    'parse_yaml_questions',
    'display_question',
    'show_result',
    'show_summary',
    'get_user_answer',
]

__version__ = '1.0.0'
