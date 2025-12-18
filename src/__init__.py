"""
MCQ TUI Package
A Rich-based TUI for answering multiple choice questions from YAML files.
"""

from .question import Question
from .parser import parse_yaml_questions
from .display import display_question, show_result, show_summary
from .input_handlers import get_user_answer
from .constants import QuestionType, NavCommand
from .console import console
from .terminal import raw_terminal
from .navigation import format_navigation_hints, handle_arrow_keys, handle_navigation_command
from .answer_formatting import (
    format_yesno_answer,
    format_single_answer,
    format_multi_answer,
    get_answer_display_text,
    get_answer_summary_text,
)

__all__ = [
    'Question',
    'parse_yaml_questions',
    'display_question',
    'show_result',
    'show_summary',
    'get_user_answer',
    'QuestionType',
    'NavCommand',
    'console',
    'raw_terminal',
    'format_navigation_hints',
    'handle_arrow_keys',
    'handle_navigation_command',
    'format_yesno_answer',
    'format_single_answer',
    'format_multi_answer',
    'get_answer_display_text',
    'get_answer_summary_text',
]

__version__ = '1.0.0'
