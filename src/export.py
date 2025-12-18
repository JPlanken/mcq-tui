"""
Export functionality for saving quiz results
"""

from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .question import Question
from .console import console
from .constants import QuestionType

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def _format_answer_for_yaml(question: Question) -> Any:
    """
    Format answer for YAML export based on question type.
    
    Returns:
        Answer value formatted for YAML (dict, list, or string)
    """
    if question.question_type == QuestionType.MULTI:
        if question.user_answers:
            return {
                "selected_indices": sorted(question.user_answers),
                "selected_options": [question.options[i - 1] for i in sorted(question.user_answers)]
            }
        return None
    elif question.question_type == QuestionType.YESNO:
        if question.user_answer == 1:
            return "Yes"
        elif question.user_answer == 2:
            return "No"
        elif question.user_answer == 3 and question.other_answer:
            return {"type": "Other", "value": question.other_answer}
        return None
    else:  # single select
        if question.user_answer == 0 and question.other_answer:
            return {"type": "Other", "value": question.other_answer}
        elif question.user_answer is not None:
            return {
                "index": question.user_answer,
                "option": question.options[question.user_answer - 1]
            }
        return None


def export_results_to_yaml(questions: List[Question], yaml_path: Path) -> bool:
    """
    Export quiz results back to the original YAML file by adding answer fields.
    
    Args:
        questions: List of Question objects with answers
        yaml_path: Path to the original YAML file
    
    Returns:
        True if export was successful, False otherwise
    """
    if not YAML_AVAILABLE:
        console.print("[red]YAML support not available. Install pyyaml: pip install pyyaml[/red]")
        return False
    
    try:
        # Read original YAML file
        content = yaml_path.read_text(encoding='utf-8')
        data = yaml.safe_load(content)
        
        if not isinstance(data, dict) or 'questions' not in data:
            console.print("[red]Invalid YAML structure: 'questions' key not found[/red]")
            return False
        
        # Match questions by ID or by index
        # First, create a mapping by ID
        question_by_id = {}
        question_by_index = {}
        for idx, q in enumerate(questions):
            if q.question_id is not None:
                question_by_id[str(q.question_id)] = q
            question_by_index[idx] = q
        
        # Add answers to each question in the YAML data
        for idx, q_data in enumerate(data['questions']):
            question = None
            question_id = q_data.get('id')
            
            # Try to match by ID first
            if question_id is not None:
                question = question_by_id.get(str(question_id))
            
            # Fall back to index matching if ID didn't work
            if question is None and idx < len(questions):
                question = question_by_index.get(idx)
            
            if question is not None:
                answer = _format_answer_for_yaml(question)
                if answer is not None:
                    q_data['answer'] = answer
        
        # Add metadata about when answers were saved
        if 'metadata' not in data:
            data['metadata'] = {}
        data['metadata']['last_answered'] = datetime.now().isoformat()
        data['metadata']['answered_count'] = sum(1 for q in questions if q.is_answered())
        data['metadata']['total_questions'] = len(questions)
        
        # Write back to file with nice formatting
        yaml_path.write_text(
            yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True),
            encoding='utf-8'
        )
        
        return True
    except yaml.YAMLError as e:
        console.print(f"[red]Error parsing YAML file: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Error exporting results: {e}[/red]")
        return False
