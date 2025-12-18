"""
Constants for question types and navigation commands
"""

from enum import Enum


class QuestionType(str, Enum):
    """Question type constants"""
    SINGLE = "single"
    MULTI = "multi"
    YESNO = "yesno"


class NavCommand(str, Enum):
    """Navigation command constants"""
    QUIT = "q"
    JUMP = "j"
    SUMMARY = "s"
    PREVIOUS = "p"
    NEXT = "n"
