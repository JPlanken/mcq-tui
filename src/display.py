"""
Display functions for questions and results
"""

from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .question import Question

console = Console()


def display_question(question: Question, question_num: int = 0, total: int = 0):
    """Display a question with options"""
    console.clear()
    
    # Header with answer status
    answered_status = ""
    if question.question_type == "multi":
        if question.user_answers:
            selected = ", ".join([str(a) for a in sorted(question.user_answers)])
            answered_status = f" [green]✓ Selected: {selected} ({len(question.user_answers)} option{'s' if len(question.user_answers) > 1 else ''})[/green]"
        else:
            answered_status = " [yellow]○ Not answered[/yellow]"
    elif question.question_type == "yesno":
        if question.user_answer == "y" or question.user_answer == 1:
            answered_status = " [green]✓ Answered: Yes (1)[/green]"
        elif question.user_answer == "n" or question.user_answer == 2:
            answered_status = " [green]✓ Answered: No (2)[/green]"
        elif question.other_answer or question.user_answer == 3:
            answered_status = f" [green]✓ Answered: Other (3): {question.other_answer}[/green]"
        else:
            answered_status = " [yellow]○ Not answered[/yellow]"
    else:  # single
        if question.user_answer is not None:
            if question.user_answer == 0:
                answered_status = f" [green]✓ Answered: Other: {question.other_answer}[/green]"
            else:
                answered_status = f" [green]✓ Answered: Option {question.user_answer}[/green]"
        else:
            answered_status = " [yellow]○ Not answered[/yellow]"
    
    # Show question type badge
    type_badge = {
        "single": "[dim][single-select][/dim]",
        "multi": "[dim][multi-select][/dim]",
        "yesno": "[dim][yes/no][/dim]"
    }.get(question.question_type, "")
    
    if question_num > 0:
        console.print(f"\n[bold cyan]Question {question_num} of {total}[/bold cyan] {type_badge}{answered_status}\n")
    else:
        console.print(f"\n{type_badge}{answered_status}\n")
    
    # Question text with type indicator
    type_label = {
        "multi": "multi-select",
        "yesno": "yes/no",
        "single": "single-select"
    }.get(question.question_type, "")
    
    # Use subtitle for type if available, otherwise include in title
    panel_kwargs = {
        "border_style": "blue",
        "padding": (1, 2),
    }
    
    if type_label:
        # Rich Panel supports subtitle parameter
        panel_kwargs["title"] = "Question"
        panel_kwargs["subtitle"] = f"[dim]{type_label}[/dim]"
    else:
        panel_kwargs["title"] = "Question"
    
    console.print(Panel(
        question.question_text,
        **panel_kwargs
    ))
    
    console.print()  # Blank line
    
    # Options table
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Choice", style="cyan", width=8)
    table.add_column("Option", style="white")
    
    if question.question_type == "yesno":
        # Yes/No/Other display with numbers
        if question.user_answer == "y" or question.user_answer == 1:
            table.add_row("[bold green]1[/bold green] [bold green]✓[/bold green]", "[bold green]Yes[/bold green]")
        else:
            table.add_row("[bold]1[/bold]", "[dim]Yes[/dim]")
        
        if question.user_answer == "n" or question.user_answer == 2:
            table.add_row("[bold green]2[/bold green] [bold green]✓[/bold green]", "[bold green]No[/bold green]")
        else:
            table.add_row("[bold]2[/bold]", "[dim]No[/dim]")
        
        if question.other_answer or question.user_answer == 3:
            if question.other_answer:
                table.add_row("[bold green]3[/bold green] [bold green]✓[/bold green]", f"[bold green]Other: {question.other_answer}[/bold green]")
            else:
                table.add_row("[bold green]3[/bold green]", "[bold green]Other (specify)[/bold green]")
        else:
            table.add_row("[bold]3[/bold]", "[dim]Other (specify)[/dim]")
    else:
        # Show numbered options (1, 2, 3...)
        for idx, option in enumerate(question.options, 1):
            # Highlight current answer if selected
            if question.question_type == "multi":
                if idx in question.user_answers:
                    table.add_row(f"[bold green]{idx}[/bold green] [bold green]✓[/bold green]", f"[bold green]{option}[/bold green]")
                else:
                    table.add_row(f"[bold]{idx}[/bold]", f"[dim]{option}[/dim]")
            else:  # single
                if question.user_answer == idx:
                    table.add_row(f"[bold green]{idx}[/bold green] [bold green]✓[/bold green]", f"[bold green]{option}[/bold green]")
                else:
                    table.add_row(f"[bold]{idx}[/bold]", f"[dim]{option}[/dim]")
        
        # Add "Other" option (0) for single-select
        if question.question_type == "single":
            if question.user_answer == 0:
                table.add_row("[bold green]0[/bold green] [bold green]✓[/bold green]", f"[bold green]Other: {question.other_answer}[/bold green]")
            else:
                table.add_row("[bold]0[/bold]", "[dim]Other (specify)[/dim]")
    
    console.print(table)
    console.print()


def show_result(question: Question):
    """Show the answer that was selected"""
    console.print()
    
    if question.question_type == "multi":
        if question.user_answers:
            selected_options = [f"Option {a}: {question.options[a-1]}" for a in sorted(question.user_answers)]
            answer_display = "\n".join([f"[yellow]{opt}[/yellow]" for opt in selected_options])
        else:
            answer_display = "[dim]No answers selected[/dim]"
    elif question.question_type == "yesno":
        if question.user_answer == "y" or question.user_answer == 1:
            answer_display = "[yellow]Yes (1)[/yellow]"
        elif question.user_answer == "n" or question.user_answer == 2:
            answer_display = "[yellow]No (2)[/yellow]"
        elif question.other_answer or question.user_answer == 3:
            answer_display = f"[yellow]Other (3):[/yellow] {question.other_answer}"
        else:
            answer_display = "[dim]No answer selected[/dim]"
    else:  # single
        if question.user_answer == 0:
            answer_display = f"[yellow]Other:[/yellow] {question.other_answer}"
        elif question.user_answer is not None:
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
    answered = sum(1 for q in questions if q.is_answered())
    
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
        table.add_column("Type", style="dim", width=12)
        table.add_column("Question", style="white", width=40)
        table.add_column("Answer", style="yellow", width=50)
        
        for idx, question in enumerate(questions, 1):
            if question.is_answered():
                type_label = {
                    "single": "single-select",
                    "multi": "multi-select",
                    "yesno": "yes/no"
                }.get(question.question_type, "unknown")
                
                if question.question_type == "multi":
                    if question.user_answers:
                        selected = [f"{a}: {question.options[a-1]}" for a in sorted(question.user_answers)]
                        answer_text = ", ".join(selected)
                    else:
                        answer_text = "[dim]No answer[/dim]"
                elif question.question_type == "yesno":
                    if question.user_answer == "y" or question.user_answer == 1:
                        answer_text = "Yes (1)"
                    elif question.user_answer == "n" or question.user_answer == 2:
                        answer_text = "No (2)"
                    elif question.other_answer or question.user_answer == 3:
                        answer_text = f"Other (3): {question.other_answer}"
                    else:
                        answer_text = "[dim]No answer[/dim]"
                else:  # single
                    if question.user_answer == 0:
                        answer_text = f"Other: {question.other_answer}"
                    else:
                        answer_text = f"Option {question.user_answer}: {question.options[question.user_answer - 1]}"
                
                # Truncate question text if too long
                q_text = question.question_text[:37] + "..." if len(question.question_text) > 40 else question.question_text
                
                table.add_row(
                    str(idx),
                    type_label,
                    q_text,
                    answer_text
                )
        
        console.print(table)
        console.print()
