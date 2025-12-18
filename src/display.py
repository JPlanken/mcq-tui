"""
Display functions for questions and results
"""

from typing import List
from rich.panel import Panel
from rich.table import Table

from .question import Question
from .console import console
from .constants import QuestionType
from .answer_formatting import get_answer_display_text, get_answer_summary_text


def display_question(question: Question, question_num: int = 0, total: int = 0):
    """Display a question with options"""
    console.clear()
    
    answered_status = ""
    if question.question_type == QuestionType.MULTI:
        if question.user_answers:
            selected = ", ".join([str(a) for a in sorted(question.user_answers)])
            answered_status = f" [green]✓ Selected: {selected} ({len(question.user_answers)} option{'s' if len(question.user_answers) > 1 else ''})[/green]"
        else:
            answered_status = " [yellow]○ Not answered[/yellow]"
    elif question.question_type == QuestionType.YESNO:
        if question.user_answer == "y" or question.user_answer == 1:
            answered_status = " [green]✓ Answered: Yes (1)[/green]"
        elif question.user_answer == "n" or question.user_answer == 2:
            answered_status = " [green]✓ Answered: No (2)[/green]"
        elif question.other_answer or question.user_answer == 3:
            answered_status = f" [green]✓ Answered: Other (3): {question.other_answer}[/green]"
        else:
            answered_status = " [yellow]○ Not answered[/yellow]"
    else:
        if question.user_answer is not None:
            if question.user_answer == 0:
                answered_status = f" [green]✓ Answered: Other: {question.other_answer}[/green]"
            else:
                answered_status = f" [green]✓ Answered: Option {question.user_answer}[/green]"
        else:
            answered_status = " [yellow]○ Not answered[/yellow]"
    
    type_badge = {
        QuestionType.SINGLE: "[dim][single-select][/dim]",
        QuestionType.MULTI: "[dim][multi-select][/dim]",
        QuestionType.YESNO: "[dim][yes/no][/dim]"
    }.get(question.question_type, "")
    
    if question_num > 0:
        console.print(f"\n[bold cyan]Question {question_num} of {total}[/bold cyan] {type_badge}{answered_status}\n")
    else:
        console.print(f"\n{type_badge}{answered_status}\n")
    
    type_label = {
        QuestionType.MULTI: "multi-select",
        QuestionType.YESNO: "yes/no",
        QuestionType.SINGLE: "single-select"
    }.get(question.question_type, "")
    
    panel_kwargs = {
        "border_style": "blue",
        "padding": (1, 2),
    }
    
    if type_label:
        panel_kwargs["title"] = "Question"
        panel_kwargs["subtitle"] = f"[dim]{type_label}[/dim]"
    else:
        panel_kwargs["title"] = "Question"
    
    console.print(Panel(
        question.question_text,
        **panel_kwargs
    ))
    
    console.print()
    
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Choice", style="cyan", width=8)
    table.add_column("Option", style="white")
    
    if question.question_type == QuestionType.YESNO:
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
        for idx, option in enumerate(question.options, 1):
            if question.question_type == QuestionType.MULTI:
                if idx in question.user_answers:
                    table.add_row(f"[bold green]{idx}[/bold green] [bold green]✓[/bold green]", f"[bold green]{option}[/bold green]")
                else:
                    table.add_row(f"[bold]{idx}[/bold]", f"[dim]{option}[/dim]")
            else:
                if question.user_answer == idx:
                    table.add_row(f"[bold green]{idx}[/bold green] [bold green]✓[/bold green]", f"[bold green]{option}[/bold green]")
                else:
                    table.add_row(f"[bold]{idx}[/bold]", f"[dim]{option}[/dim]")
        
        if question.question_type == QuestionType.SINGLE:
            if question.user_answer == 0:
                table.add_row("[bold green]0[/bold green] [bold green]✓[/bold green]", f"[bold green]Other: {question.other_answer}[/bold green]")
            else:
                table.add_row("[bold]0[/bold]", "[dim]Other (specify)[/dim]")
    
    console.print(table)
    console.print()


def show_result(question: Question):
    """Show the answer that was selected"""
    console.print()
    
    answer_display = get_answer_display_text(question)
    
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
    
    if answered > 0:
        table = Table(title="Your Answers", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Type", style="dim", width=12)
        table.add_column("Question", style="white", width=40)
        table.add_column("Answer", style="yellow", width=50)
        
        for idx, question in enumerate(questions, 1):
            if question.is_answered():
                type_label = {
                    QuestionType.SINGLE: "single-select",
                    QuestionType.MULTI: "multi-select",
                    QuestionType.YESNO: "yes/no"
                }.get(question.question_type, "unknown")
                
                answer_text = get_answer_summary_text(question)
                
                q_text = question.question_text[:37] + "..." if len(question.question_text) > 40 else question.question_text
                
                table.add_row(
                    str(idx),
                    type_label,
                    q_text,
                    answer_text
                )
        
        console.print(table)
        console.print()
