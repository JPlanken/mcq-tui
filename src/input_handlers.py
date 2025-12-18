"""
Input handling functions for different question types
"""

import sys
import termios
import tty
from typing import Optional, Tuple
from rich.console import Console
from rich.prompt import Prompt

from .question import Question
from .display import display_question

console = Console()


def get_multi_select_answer(question: Question, question_num: int = 0, total: int = 0) -> Tuple[Optional[str], Optional[str]]:
    """
    Interactive multi-select: toggle selections with number keys, Enter to confirm.
    Returns: (answer_data, nav_command)
    """
    # Initialize selections from existing answers if any
    selected = set(question.user_answers) if question.user_answers else set()
    
    while True:
        # Redraw the question with current selections
        display_question(question, question_num, total)
        
        # Show current selection count
        if selected:
            count_text = f"[green]{len(selected)} selected[/green]"
        else:
            count_text = "[dim]No selections[/dim]"
        
        console.print(f"\n[dim]Press number keys (1-{len(question.options)}) to toggle, Enter to confirm:[/dim] {count_text}")
        nav_hints = []
        if question_num > 1:
            nav_hints.append("[dim]← = previous[/dim]")
        if question_num < total:
            nav_hints.append("[dim]→ = next[/dim]")
        nav_hints.append("[dim]'j' = jump[/dim]")
        nav_hints.append("[dim]'s' = summary[/dim]")
        nav_hints.append("[dim]'q' = quit[/dim]")
        console.print("  ".join(nav_hints) + "\n")
        
        # Get single character input
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            # Handle Ctrl+C
            if ch == '\x03':  # Ctrl+C
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                raise KeyboardInterrupt
            
            # Handle arrow keys and Enter
            if ch == '\x1b':  # ESC character
                ch2 = sys.stdin.read(1)
                if ch2 == '[':  # CSI
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'D':  # Left arrow
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        return None, 'p'
                    elif ch3 == 'C':  # Right arrow
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        # Return answer if selected, otherwise just navigate
                        if selected:
                            return ",".join([str(n) for n in sorted(selected)]), None
                        return None, 'n'
            elif ch == '\r' or ch == '\n':  # Enter
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                # Return current selections
                if selected:
                    return ",".join([str(n) for n in sorted(selected)]), None
                else:
                    # No selections, treat as next
                    return None, 'n'
            elif ch == 'q':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return None, 'q'
            elif ch == 'j':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return None, 'j'
            elif ch == 's':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return None, 's'
            elif ch.isdigit():
                # Toggle selection
                num = int(ch)
                if 1 <= num <= len(question.options):
                    if num in selected:
                        selected.remove(num)
                    else:
                        selected.add(num)
                    # Update question's user_answers for display immediately
                    question.user_answers = sorted(list(selected))
                    # Restore terminal before redraw
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    # Continue while loop to redraw with updated selections
                    continue
                else:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    console.print(f"[red]Invalid choice. Press 1-{len(question.options)}[/red]")
                    input("\nPress Enter to continue...")
                    # Continue loop after error message
                    continue
            else:
                # Ignore other characters - restore terminal and continue loop
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                # Continue loop to wait for valid input
                continue
        except KeyboardInterrupt:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            raise  # Re-raise to be handled by caller
        except Exception:
            # Ensure terminal is restored on any unexpected error
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass
            raise
        finally:
            # Safety net: ensure terminal is always restored
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass


def get_single_select_answer(question: Question, question_num: int = 0, total: int = 0) -> Tuple[Optional[str], Optional[str]]:
    """
    Interactive single-select: press number key to select, Enter to confirm.
    Returns: (answer_data, nav_command)
    """
    while True:
        # Redraw the question with current selection
        display_question(question, question_num, total)
        
        # Show instructions
        if question.user_answer is not None:
            console.print(f"\n[green]Selected: {question.user_answer}[/green] [dim]- Press Enter to confirm[/dim]")
        else:
            console.print(f"\n[dim]Press number key (0-{len(question.options)}) to select, Enter to confirm[/dim]")
        nav_hints = []
        if question_num > 1:
            nav_hints.append("[dim]← = previous[/dim]")
        if question_num < total:
            nav_hints.append("[dim]→ = next[/dim]")
        nav_hints.append("[dim]'j' = jump[/dim]")
        nav_hints.append("[dim]'s' = summary[/dim]")
        nav_hints.append("[dim]'q' = quit[/dim]")
        console.print("  ".join(nav_hints) + "\n")
        
        # Get single character input
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            # Handle Ctrl+C
            if ch == '\x03':  # Ctrl+C
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                raise KeyboardInterrupt
            
            # Handle arrow keys and Enter
            if ch == '\x1b':  # ESC character
                ch2 = sys.stdin.read(1)
                if ch2 == '[':  # CSI
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'D':  # Left arrow
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        return None, 'p'
                    elif ch3 == 'C':  # Right arrow
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        # Return current answer if selected, otherwise next
                        if question.user_answer is not None:
                            if question.user_answer == 0:
                                return f"0:{question.other_answer}", None
                            return str(question.user_answer), None
                        return None, 'n'
            elif ch == '\r' or ch == '\n':  # Enter
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                # Return current selection if any
                if question.user_answer is not None:
                    if question.user_answer == 0:
                        return f"0:{question.other_answer}", None
                    return str(question.user_answer), None
                # No selection, treat as next
                return None, 'n'
            elif ch == 'q':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return None, 'q'
            elif ch == 'j':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return None, 'j'
            elif ch == 's':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return None, 's'
            elif ch.isdigit():
                # Select option (but don't return yet - wait for Enter)
                num = int(ch)
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
                if num < 0 or num > len(question.options):
                    console.print(f"[red]Invalid choice. Press 0-{len(question.options)}[/red]")
                    input("\nPress Enter to continue...")
                    continue
                
                if num == 0:
                    # "Other" option - get free text input
                    other_text = Prompt.ask("Enter your answer (Other)")
                    question.user_answer = 0
                    question.other_answer = other_text.strip()
                    # After getting "other" text, still need Enter to confirm
                    # Continue loop to show selection and wait for Enter
                    continue
                else:
                    # Regular option (1-N) - update selection but wait for Enter
                    question.user_answer = num
                    question.other_answer = None
                    # Continue loop to redraw with updated selection
                    continue
            else:
                # Ignore other characters
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                continue
        except KeyboardInterrupt:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            raise
        except Exception:
            # Ensure terminal is restored on any unexpected error
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass
            raise
        finally:
            # Safety net: ensure terminal is always restored
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass


def get_yesno_answer(question: Question, question_num: int = 0, total: int = 0) -> Tuple[Optional[str], Optional[str]]:
    """
    Interactive yes/no: press 1/2/3 or y/n/o to select, Enter to confirm.
    Returns: (answer_data, nav_command)
    """
    while True:
        # Redraw the question with current selection
        display_question(question, question_num, total)
        
        # Show instructions
        if question.user_answer is not None:
            answer_text = {1: "Yes", 2: "No", 3: f"Other: {question.other_answer}"}.get(question.user_answer, str(question.user_answer))
            console.print(f"\n[green]Selected: {answer_text}[/green] [dim]- Press Enter to confirm[/dim]")
        else:
            console.print("\n[dim]Press 1 (Yes), 2 (No), 3 (Other), then Enter to confirm[/dim]")
        nav_hints = []
        if question_num > 1:
            nav_hints.append("[dim]← = previous[/dim]")
        if question_num < total:
            nav_hints.append("[dim]→ = next[/dim]")
        nav_hints.append("[dim]'j' = jump[/dim]")
        nav_hints.append("[dim]'s' = summary[/dim]")
        nav_hints.append("[dim]'q' = quit[/dim]")
        console.print("  ".join(nav_hints) + "\n")
        
        # Get single character input
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            # Handle Ctrl+C
            if ch == '\x03':  # Ctrl+C
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                raise KeyboardInterrupt
            
            # Handle arrow keys and Enter
            if ch == '\x1b':  # ESC character
                ch2 = sys.stdin.read(1)
                if ch2 == '[':  # CSI
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'D':  # Left arrow
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        return None, 'p'
                    elif ch3 == 'C':  # Right arrow
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        # Return current answer if selected
                        if question.user_answer == 1 or question.user_answer == "y":
                            return "1", None
                        elif question.user_answer == 2 or question.user_answer == "n":
                            return "2", None
                        elif question.other_answer or question.user_answer == 3:
                            return f"3:{question.other_answer}", None
                        return None, 'n'
            elif ch == '\r' or ch == '\n':  # Enter
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                # Return current selection if any
                if question.user_answer == 1 or question.user_answer == "y":
                    return "1", None
                elif question.user_answer == 2 or question.user_answer == "n":
                    return "2", None
                elif question.other_answer or question.user_answer == 3:
                    return f"3:{question.other_answer}", None
                # No selection, treat as next
                return None, 'n'
            elif ch == 'q':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return None, 'q'
            elif ch == 'j':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return None, 'j'
            elif ch == 's':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return None, 's'
            elif ch in ['1', 'y', 'Y']:
                # Yes selected (but wait for Enter to confirm)
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                question.user_answer = 1
                question.other_answer = None
                # Continue loop to redraw with updated selection
                continue
            elif ch in ['2', 'n', 'N']:
                # No selected (but wait for Enter to confirm)
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                question.user_answer = 2
                question.other_answer = None
                # Continue loop to redraw with updated selection
                continue
            elif ch in ['3', 'o', 'O']:
                # Other selected - get free text input
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                other_text = Prompt.ask("Enter your answer (Other)")
                question.user_answer = 3
                question.other_answer = other_text.strip()
                # After getting "other" text, still need Enter to confirm
                # Continue loop to show selection and wait for Enter
                continue
            else:
                # Ignore other characters
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                continue
        except KeyboardInterrupt:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            raise
        except Exception:
            # Ensure terminal is restored on any unexpected error
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass
            raise
        finally:
            # Safety net: ensure terminal is always restored
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass


def get_user_answer(question: Question, question_num: int = 0, total: int = 0) -> Tuple[Optional[str], Optional[str]]:
    """
    Get user's answer choice or navigation command.
    Returns: (answer_data, nav_command)
    - answer_data: depends on question type
    - nav_command: 'n' (next), 'p' (previous), 'j' (jump), 's' (summary), 'q' (quit), None
    """
    # All question types now use interactive mode with immediate visual feedback
    if question.question_type == "multi":
        return get_multi_select_answer(question, question_num, total)
    elif question.question_type == "yesno":
        return get_yesno_answer(question, question_num, total)
    else:  # single
        return get_single_select_answer(question, question_num, total)
