"""
Navigation utilities for handling user input and commands
"""

import sys
from typing import Optional, Tuple

from .constants import NavCommand


def format_navigation_hints(question_num: int, total: int) -> str:
    """
    Format navigation hints based on current question position.
    
    Args:
        question_num: Current question number (1-based)
        total: Total number of questions
        
    Returns:
        Formatted string with navigation hints
    """
    nav_hints = []
    if question_num > 1:
        nav_hints.append("[dim]← = previous[/dim]")
    if question_num < total:
        nav_hints.append("[dim]→ = next[/dim]")
    nav_hints.append("[dim]'j' = jump[/dim]")
    nav_hints.append("[dim]'s' = summary[/dim]")
    nav_hints.append("[dim]'q' = quit[/dim]")
    return "  ".join(nav_hints)


def handle_arrow_keys(ch: str) -> Optional[str]:
    """
    Handle arrow key sequences.
    
    Args:
        ch: First character of input sequence
        
    Returns:
        Navigation command ('p' for left, 'n' for right) or None
    """
    if ch == '\x1b':  # ESC character
        ch2 = sys.stdin.read(1)
        if ch2 == '[':  # CSI
            ch3 = sys.stdin.read(1)
            if ch3 == 'D':  # Left arrow
                return NavCommand.PREVIOUS
            elif ch3 == 'C':  # Right arrow
                return NavCommand.NEXT
    return None


def handle_navigation_command(ch: str) -> Optional[str]:
    """
    Handle single-character navigation commands.
    
    Args:
        ch: Input character
        
    Returns:
        Navigation command string or None
    """
    if ch == NavCommand.QUIT:
        return NavCommand.QUIT
    elif ch == NavCommand.JUMP:
        return NavCommand.JUMP
    elif ch == NavCommand.SUMMARY:
        return NavCommand.SUMMARY
    elif ch == '\r' or ch == '\n':  # Enter
        return NavCommand.NEXT
    return None
