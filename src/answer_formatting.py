"""
Answer formatting utilities for consistent display across modules
"""

from typing import Optional, Tuple

from .question import Question
from .constants import QuestionType


def format_yesno_answer(question: Question) -> Tuple[Optional[str], Optional[str]]:
    """
    Format yes/no answer for display or return.
    
    Returns:
        Tuple of (answer_string, other_answer_text)
    """
    if question.user_answer == 1 or question.user_answer == "y":
        return "1", None
    elif question.user_answer == 2 or question.user_answer == "n":
        return "2", None
    elif question.other_answer or question.user_answer == 3:
        return f"3:{question.other_answer}", question.other_answer
    return None, None


def format_single_answer(question: Question) -> Tuple[Optional[str], Optional[str]]:
    """
    Format single-select answer for display or return.
    
    Returns:
        Tuple of (answer_string, other_answer_text)
    """
    if question.user_answer is not None:
        if question.user_answer == 0:
            return f"0:{question.other_answer}", question.other_answer
        return str(question.user_answer), None
    return None, None


def format_multi_answer(question: Question) -> Optional[str]:
    """
    Format multi-select answer for display or return.
    
    Returns:
        Comma-separated string of selected option numbers or None
    """
    if question.user_answers:
        return ",".join([str(n) for n in sorted(question.user_answers)])
    return None


def get_answer_display_text(question: Question) -> str:
    """
    Get formatted answer text for display in results/summary.
    
    Returns:
        Formatted answer text string
    """
    if question.question_type == QuestionType.MULTI:
        if question.user_answers:
            selected_options = [f"Option {a}: {question.options[a-1]}" for a in sorted(question.user_answers)]
            return "\n".join([f"[yellow]{opt}[/yellow]" for opt in selected_options])
        return "[dim]No answers selected[/dim]"
    elif question.question_type == QuestionType.YESNO:
        answer_str, other = format_yesno_answer(question)
        if answer_str == "1":
            return "[yellow]Yes (1)[/yellow]"
        elif answer_str == "2":
            return "[yellow]No (2)[/yellow]"
        elif answer_str and answer_str.startswith("3:"):
            return f"[yellow]Other (3):[/yellow] {other}"
        return "[dim]No answer selected[/dim]"
    else:  # single
        if question.user_answer == 0:
            return f"[yellow]Other:[/yellow] {question.other_answer}"
        elif question.user_answer is not None:
            return f"[yellow]Option {question.user_answer}:[/yellow] {question.options[question.user_answer - 1]}"
        return "[dim]No answer selected[/dim]"


def get_answer_summary_text(question: Question) -> str:
    """
    Get formatted answer text for summary table (no Rich markup).
    
    Returns:
        Plain text answer string
    """
    if question.question_type == QuestionType.MULTI:
        if question.user_answers:
            selected = [f"{a}: {question.options[a-1]}" for a in sorted(question.user_answers)]
            return ", ".join(selected)
        return "[dim]No answer[/dim]"
    elif question.question_type == QuestionType.YESNO:
        answer_str, other = format_yesno_answer(question)
        if answer_str == "1":
            return "Yes (1)"
        elif answer_str == "2":
            return "No (2)"
        elif answer_str and answer_str.startswith("3:"):
            return f"Other (3): {other}"
        return "[dim]No answer[/dim]"
    else:  # single
        if question.user_answer == 0:
            return f"Other: {question.other_answer}"
        else:
            return f"Option {question.user_answer}: {question.options[question.user_answer - 1]}"
