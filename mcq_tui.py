#!/usr/bin/env python3
"""
Multiple Choice Question TUI
A Rich-based TUI for answering multiple choice questions from YAML files.
"""

import sys
import termios
import tty
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.markdown import Markdown  # Used for displaying format examples

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

console = Console()


class Question:
    """Represents a multiple choice question"""
    
    def __init__(self, question_text: str, options: List[str]):
        self.question_text = question_text.strip()
        self.options = [opt.strip() for opt in options]
        self.user_answer: Optional[int] = None  # Option number (1-N) or None
        self.other_answer: Optional[str] = None  # Free text if user chose "Other" (0)


def parse_yaml_questions(file_path: Path) -> List[Question]:
    """Parse YAML format questions"""
    if not YAML_AVAILABLE:
        console.print("[red]YAML support not available. Install pyyaml: pip install pyyaml[/red]")
        return []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        data = yaml.safe_load(content)
        
        questions = []
        if 'questions' in data:
            for q_data in data['questions']:
                question_text = q_data.get('question', '').strip()
                options = q_data.get('options', [])
                
                if question_text and options:
                    questions.append(Question(question_text, options))
        
        return questions
    except yaml.YAMLError as e:
        console.print(f"[red]Error parsing YAML file: {e}[/red]")
        return []
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return []


def display_question(question: Question, question_num: int, total: int):
    """Display a question with options"""
    console.clear()
    
    # Header with answer status
    answered_status = ""
    if question.user_answer is not None:
        if question.user_answer == 0:
            answered_status = f" [green]✓ Answered: Other: {question.other_answer}[/green]"
        else:
            answered_status = f" [green]✓ Answered: Option {question.user_answer}[/green]"
    else:
        answered_status = " [yellow]○ Not answered[/yellow]"
    
    console.print(f"\n[bold cyan]Question {question_num} of {total}[/bold cyan]{answered_status}\n")
    
    # Question text
    console.print(Panel(
        question.question_text,
        title="Question",
        border_style="blue",
        padding=(1, 2)
    ))
    
    console.print()  # Blank line
    
    # Options table
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Choice", style="cyan", width=8)
    table.add_column("Option", style="white")
    
    # Show numbered options (1, 2, 3...)
    for idx, option in enumerate(question.options, 1):
        # Highlight current answer if selected
        if question.user_answer == idx:
            table.add_row(f"[bold green]{idx}[/bold green]", f"[green]{option}[/green]")
        else:
            table.add_row(f"[bold]{idx}[/bold]", option)
    
    # Add "Other" option (0)
    if question.user_answer == 0:
        table.add_row("[bold green]0[/bold green]", f"[green]Other: {question.other_answer}[/green]")
    else:
        table.add_row("[bold]0[/bold]", "[dim]Other (specify)[/dim]")
    
    console.print(table)
    console.print()
    
    # Navigation hints
    nav_hints = []
    if question_num < total:
        nav_hints.append("[dim]→ or Enter = next[/dim]")
    if question_num > 1:
        nav_hints.append("[dim]← = previous[/dim]")
    nav_hints.append("[dim]'j' = jump[/dim]")
    nav_hints.append("[dim]'s' = summary[/dim]")
    nav_hints.append("[dim]'q' = quit[/dim]")
    
    if nav_hints:
        console.print("  ".join(nav_hints))
        console.print()


def get_user_input_with_arrows():
    """Get user input, handling arrow keys and regular input"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        
        # Read first character
        ch = sys.stdin.read(1)
        
        # Check for escape sequence (arrow keys)
        if ch == '\x1b':  # ESC character
            ch2 = sys.stdin.read(1)
            if ch2 == '[':  # CSI (Control Sequence Introducer)
                ch3 = sys.stdin.read(1)
                if ch3 == 'D':  # Left arrow
                    return 'LEFT'
                elif ch3 == 'C':  # Right arrow
                    return 'RIGHT'
                elif ch3 == 'A':  # Up arrow
                    return 'UP'
                elif ch3 == 'B':  # Down arrow
                    return 'DOWN'
        elif ch == '\r' or ch == '\n':  # Enter key
            return '\n'
        elif ch == '\x7f':  # Backspace
            return '\b'
        
        # For regular characters, read the rest of the line
        result = ch
        while True:
            next_ch = sys.stdin.read(1)
            if next_ch == '\r' or next_ch == '\n':
                break
            elif next_ch == '\x7f':  # Backspace
                if len(result) > 0:
                    result = result[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                result += next_ch
                sys.stdout.write(next_ch)
                sys.stdout.flush()
        
        return result
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_user_answer(num_options: int) -> Tuple[Optional[int], Optional[str], Optional[str]]:
    """
    Get user's answer choice or navigation command.
    Returns: (option_number, other_text, nav_command)
    - option_number: 1-N for regular options, 0 for "Other", None if navigation
    - other_text: text input if option 0 was chosen, None otherwise
    - nav_command: 'n' (next), 'p' (previous), 'j' (jump), 's' (summary), 'q' (quit), None
    """
    while True:
        console.print("[dim]Enter your answer (or ←/→ arrows, Enter for next):[/dim] ", end="")
        
        choice = get_user_input_with_arrows()
        console.print()  # New line
        
        # Handle arrow keys and Enter
        if choice == 'RIGHT' or choice == '\n':
            return None, None, 'n'
        elif choice == 'LEFT':
            return None, None, 'p'
        
        choice_str = choice.strip().lower()
        
        # Navigation commands
        if choice_str in ['n', 'p', 'j', 's', 'q']:
            return None, None, choice_str
        
        # Validate numeric input
        try:
            choice_num = int(choice_str)
            
            if choice_num < 0 or choice_num > num_options:
                console.print(f"[red]Invalid choice. Please enter 0-{num_options} or use arrows/navigation commands[/red]")
                continue
            
            if choice_num == 0:
                # "Other" option - get free text input
                other_text = Prompt.ask("Enter your answer (Other)")
                return 0, other_text, None
            else:
                # Regular option (1-N)
                return choice_num, None, None
        except ValueError:
            console.print("[red]Invalid input. Use number (0-{}), arrows (←/→), or commands (n/p/j/s/q)[/red]".format(num_options))
            continue


def show_result(question: Question):
    """Show the answer that was selected"""
    console.print()
    
    if question.user_answer == 0:
        # "Other" option was chosen
        answer_display = f"[yellow]Other:[/yellow] {question.other_answer}"
    elif question.user_answer is not None:
        # Regular option was chosen
        answer_display = f"[yellow]Option {question.user_answer}:[/yellow] {question.options[question.user_answer - 1]}"
    else:
        answer_display = "[dim]No answer selected[/dim]"
    
    console.print(Panel(
        f"[bold]Answer recorded:[/bold]\n{answer_display}",
        border_style="blue",
        padding=(0, 2)
    ))
    
    console.print()


def show_summary(questions: List[Question]):
    """Show final summary of answers"""
    console.clear()
    
    total = len(questions)
    answered = sum(1 for q in questions if q.user_answer is not None)
    
    # Summary panel
    summary_text = (
        f"[bold]Total Questions:[/bold] {total}\n"
        f"[bold]Answered:[/bold] {answered}\n"
    )
    
    console.print(Panel(
        summary_text,
        title="Summary",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    console.print()
    
    # Detailed results table
    if answered > 0:
        table = Table(title="Your Answers", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Question", style="white", width=40)
        table.add_column("Answer", style="yellow", width=50)
        
        for idx, question in enumerate(questions, 1):
            if question.user_answer is not None:
                if question.user_answer == 0:
                    answer_text = f"Other: {question.other_answer}"
                else:
                    answer_text = f"Option {question.user_answer}: {question.options[question.user_answer - 1]}"
                
                # Truncate question text if too long
                q_text = question.question_text[:37] + "..." if len(question.question_text) > 40 else question.question_text
                
                table.add_row(
                    str(idx),
                    q_text,
                    answer_text
                )
        
        console.print(table)
        console.print()


def main():
    """Main application loop"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Multiple Choice Question TUI - Interactive terminal UI for answering questions from YAML files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Format: YAML (.yaml, .yml)

Example:
  mcq questions.yaml
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Path to YAML question file'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    console.print("[bold cyan]Multiple Choice Question TUI[/bold cyan]\n")
    
    # Get file path
    if args.file:
        file_path = Path(args.file)
    else:
        file_input = Prompt.ask("Enter path to YAML question file")
        file_path = Path(file_input)
    
    if not file_path.exists():
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        return
    
    # Parse questions
    console.print(f"\n[dim]Parsing YAML questions from {file_path}...[/dim]")
    questions = parse_yaml_questions(file_path)
    
    if not questions:
        console.print("[red]No questions found in file![/red]")
        console.print("\n[yellow]Expected YAML format:[/yellow]")
        console.print(Markdown("""
```yaml
questions:
  - question: "What is the capital of France?"
    options:
      - "London"
      - "Paris"
      - "Berlin"
      - "Madrid"
```
        """))
        return
    
    console.print(f"[green]Found {len(questions)} question(s)[/green]\n")
    
    # Main navigation loop
    current_idx = 0  # 0-based index
    total = len(questions)
    
    while True:
        # Display current question
        display_question(questions[current_idx], current_idx + 1, total)
        
        # Get user input (answer or navigation)
        user_answer, other_text, nav_command = get_user_answer(len(questions[current_idx].options))
        
        # Handle navigation commands
        if nav_command == 'q':
            if Confirm.ask("\n[yellow]Quit quiz?[/yellow]", default=True):
                break
            continue
        elif nav_command == 's':
            show_summary(questions)
            if not Confirm.ask("\n[dim]Return to questions?[/dim]", default=True):
                break
            continue
        elif nav_command == 'j':
            # Jump to specific question
            try:
                target = Prompt.ask(f"Jump to question (1-{total})", default=str(current_idx + 1))
                target_num = int(target)
                if 1 <= target_num <= total:
                    current_idx = target_num - 1
                else:
                    console.print(f"[red]Invalid question number. Must be between 1 and {total}[/red]")
                    input("\nPress Enter to continue...")
            except ValueError:
                console.print("[red]Invalid input[/red]")
                input("\nPress Enter to continue...")
            continue
        elif nav_command == 'p':
            # Previous question
            if current_idx > 0:
                current_idx -= 1
            continue
        elif nav_command == 'n':
            # Next question
            if current_idx < total - 1:
                current_idx += 1
            else:
                # Reached end, show summary
                show_summary(questions)
                break
            continue
        
        # Handle answer input
        if user_answer is not None:
            questions[current_idx].user_answer = user_answer
            questions[current_idx].other_answer = other_text
            show_result(questions[current_idx])
            
            # Auto-advance to next question after answering
            if current_idx < total - 1:
                current_idx += 1
            else:
                # Last question answered, show summary
                show_summary(questions)
                break
        elif nav_command is None:
            # Empty input or invalid - treat as next
            if current_idx < total - 1:
                current_idx += 1
            else:
                show_summary(questions)
                break
    
    console.print("\n[dim]Press Enter to exit...[/dim]")
    input()


if __name__ == "__main__":
    main()

