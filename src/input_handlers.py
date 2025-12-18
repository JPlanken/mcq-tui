"""
Input handling functions for different question types
"""

import sys
from typing import Optional, Tuple
from rich.prompt import Prompt

from .question import Question
from .display import display_question
from .console import console
from .terminal import raw_terminal
from .navigation import format_navigation_hints, handle_arrow_keys, handle_navigation_command
from .answer_formatting import format_multi_answer, format_single_answer, format_yesno_answer
from .constants import QuestionType, NavCommand


def get_multi_select_answer(question: Question, question_num: int = 0, total: int = 0) -> Tuple[Optional[str], Optional[str]]:
    """
    Interactive multi-select: toggle selections with number keys, Enter to confirm.
    Returns: (answer_data, nav_command)
    """
    selected = set(question.user_answers) if question.user_answers else set()
    
    while True:
        display_question(question, question_num, total)
        
        if selected:
            count_text = f"[green]{len(selected)} selected[/green]"
        else:
            count_text = "[dim]No selections[/dim]"
        
        console.print(f"\n[dim]Press number keys (1-{len(question.options)}) to toggle, Enter to confirm:[/dim] {count_text}")
        console.print(format_navigation_hints(question_num, total) + "\n")
        
        ch = None
        with raw_terminal():
            ch = sys.stdin.read(1)
            
            if ch == '\x03':
                raise KeyboardInterrupt
            
            arrow_cmd = handle_arrow_keys(ch)
            if arrow_cmd == NavCommand.PREVIOUS:
                return None, NavCommand.PREVIOUS
            elif arrow_cmd == NavCommand.NEXT:
                answer = format_multi_answer(question)
                return answer, None if answer else NavCommand.NEXT
            
            nav_cmd = handle_navigation_command(ch)
            if nav_cmd == NavCommand.QUIT:
                return None, NavCommand.QUIT
            elif nav_cmd == NavCommand.JUMP:
                return None, NavCommand.JUMP
            elif nav_cmd == NavCommand.SUMMARY:
                return None, NavCommand.SUMMARY
            elif nav_cmd == NavCommand.NEXT:
                answer = format_multi_answer(question)
                return answer, None if answer else NavCommand.NEXT
            
            if ch.isdigit():
                num = int(ch)
                if 1 <= num <= len(question.options):
                    if num in selected:
                        selected.remove(num)
                    else:
                        selected.add(num)
                    question.user_answers = sorted(list(selected))
                    continue
        
        if ch and ch.isdigit():
            num = int(ch)
            if num < 1 or num > len(question.options):
                console.print(f"[red]Invalid choice. Press 1-{len(question.options)}[/red]")
                input("\nPress Enter to continue...")
                continue


def get_single_select_answer(question: Question, question_num: int = 0, total: int = 0) -> Tuple[Optional[str], Optional[str]]:
    """
    Interactive single-select: press number key to select, Enter to confirm.
    Returns: (answer_data, nav_command)
    """
    while True:
        display_question(question, question_num, total)
        
        if question.user_answer is not None:
            console.print(f"\n[green]Selected: {question.user_answer}[/green] [dim]- Press Enter to confirm[/dim]")
        else:
            console.print(f"\n[dim]Press number key (0-{len(question.options)}) to select, Enter to confirm[/dim]")
        console.print(format_navigation_hints(question_num, total) + "\n")
        
        ch = None
        with raw_terminal():
            ch = sys.stdin.read(1)
            
            if ch == '\x03':
                raise KeyboardInterrupt
            
            arrow_cmd = handle_arrow_keys(ch)
            if arrow_cmd == NavCommand.PREVIOUS:
                return None, NavCommand.PREVIOUS
            elif arrow_cmd == NavCommand.NEXT:
                answer, _ = format_single_answer(question)
                return answer, None if answer else NavCommand.NEXT
            
            nav_cmd = handle_navigation_command(ch)
            if nav_cmd == NavCommand.QUIT:
                return None, NavCommand.QUIT
            elif nav_cmd == NavCommand.JUMP:
                return None, NavCommand.JUMP
            elif nav_cmd == NavCommand.SUMMARY:
                return None, NavCommand.SUMMARY
            elif nav_cmd == NavCommand.NEXT:
                answer, _ = format_single_answer(question)
                return answer, None if answer else NavCommand.NEXT
            
            if ch.isdigit():
                num = int(ch)
                if num < 0 or num > len(question.options):
                    continue
        
        if ch and ch.isdigit():
            num = int(ch)
            if num < 0 or num > len(question.options):
                console.print(f"[red]Invalid choice. Press 0-{len(question.options)}[/red]")
                input("\nPress Enter to continue...")
                continue
            
            if num == 0:
                other_text = Prompt.ask("Enter your answer (Other)")
                question.user_answer = 0
                question.other_answer = other_text.strip()
                continue
            else:
                question.user_answer = num
                question.other_answer = None
                continue


def get_yesno_answer(question: Question, question_num: int = 0, total: int = 0) -> Tuple[Optional[str], Optional[str]]:
    """
    Interactive yes/no: press 1/2/3 or y/n/o to select, Enter to confirm.
    Returns: (answer_data, nav_command)
    """
    while True:
        display_question(question, question_num, total)
        
        if question.user_answer is not None:
            answer_text = {1: "Yes", 2: "No", 3: f"Other: {question.other_answer}"}.get(question.user_answer, str(question.user_answer))
            console.print(f"\n[green]Selected: {answer_text}[/green] [dim]- Press Enter to confirm[/dim]")
        else:
            console.print("\n[dim]Press 1 (Yes), 2 (No), 3 (Other), then Enter to confirm[/dim]")
        console.print(format_navigation_hints(question_num, total) + "\n")
        
        ch = None
        with raw_terminal():
            ch = sys.stdin.read(1)
            
            if ch == '\x03':
                raise KeyboardInterrupt
            
            arrow_cmd = handle_arrow_keys(ch)
            if arrow_cmd == NavCommand.PREVIOUS:
                return None, NavCommand.PREVIOUS
            elif arrow_cmd == NavCommand.NEXT:
                answer, _ = format_yesno_answer(question)
                return answer, None if answer else NavCommand.NEXT
            
            nav_cmd = handle_navigation_command(ch)
            if nav_cmd == NavCommand.QUIT:
                return None, NavCommand.QUIT
            elif nav_cmd == NavCommand.JUMP:
                return None, NavCommand.JUMP
            elif nav_cmd == NavCommand.SUMMARY:
                return None, NavCommand.SUMMARY
            elif nav_cmd == NavCommand.NEXT:
                answer, _ = format_yesno_answer(question)
                return answer, None if answer else NavCommand.NEXT
            
            if ch in ['1', 'y', 'Y']:
                question.user_answer = 1
                question.other_answer = None
                continue
            elif ch in ['2', 'n', 'N']:
                question.user_answer = 2
                question.other_answer = None
                continue
            elif ch in ['3', 'o', 'O']:
                continue
        
        if ch and ch in ['3', 'o', 'O']:
            other_text = Prompt.ask("Enter your answer (Other)")
            question.user_answer = 3
            question.other_answer = other_text.strip()
            continue


def get_user_answer(question: Question, question_num: int = 0, total: int = 0) -> Tuple[Optional[str], Optional[str]]:
    """
    Get user's answer choice or navigation command.
    Returns: (answer_data, nav_command)
    """
    if question.question_type == QuestionType.MULTI:
        return get_multi_select_answer(question, question_num, total)
    elif question.question_type == QuestionType.YESNO:
        return get_yesno_answer(question, question_num, total)
    else:
        return get_single_select_answer(question, question_num, total)
