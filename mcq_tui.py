#!/usr/bin/env python3
"""
Multiple Choice Question TUI
Main entry point for the CLI application.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

from src import (
    parse_yaml_questions,
    display_question,
    show_summary,
    show_result,
    get_user_answer,
)


def main():
    """Main application loop"""
    import argparse
    
    console = Console()
    
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
    
    try:
        while True:
            # Display current question
            display_question(questions[current_idx], current_idx + 1, total)
            
            # Get user input (answer or navigation)
            try:
                answer_data, nav_command = get_user_answer(questions[current_idx], current_idx + 1, total)
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Interrupted by user (Ctrl+C)[/yellow]")
                raise
            
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
            # Note: Input handlers already set question attributes, so we just need to show result
            if answer_data is not None:
                question = questions[current_idx]
                show_result(question)
                
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
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Quiz interrupted by user (Ctrl+C). Exiting...[/yellow]")
        console.print()
        sys.exit(0)
    
    console.print("\n[dim]Press Enter to exit...[/dim]")
    try:
        input()
    except KeyboardInterrupt:
        console.print("\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
