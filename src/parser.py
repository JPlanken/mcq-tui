"""
YAML parsing functionality
"""

from pathlib import Path
from typing import List
from rich.console import Console

from .question import Question

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

console = Console()


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
                question_type = q_data.get('type', 'single').lower()
                options = q_data.get('options', [])
                
                # For yesno type, create default options if not provided
                if question_type == 'yesno' and not options:
                    options = ['Yes', 'No']
                
                if question_text:
                    # For yesno type, options are optional
                    if question_type == 'yesno' or options:
                        questions.append(Question(question_text, options, question_type))
        
        return questions
    except yaml.YAMLError as e:
        console.print(f"[red]Error parsing YAML file: {e}[/red]")
        return []
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return []
