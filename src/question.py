"""
Question data model
"""

from typing import List, Optional

from .constants import QuestionType


class Question:
    """Represents a question with different types"""
    
    def __init__(self, question_text: str, options: List[str], question_type: str = QuestionType.SINGLE):
        self.question_text = question_text.strip()
        self.options = [opt.strip() for opt in options]
        self.question_type = question_type.lower()
        
        self.user_answer: Optional[int] = None
        self.user_answers: List[int] = []
        self.other_answer: Optional[str] = None
    
    def is_answered(self) -> bool:
        """Check if question has been answered"""
        if self.question_type == QuestionType.MULTI:
            return len(self.user_answers) > 0
        elif self.question_type == QuestionType.YESNO:
            return self.user_answer is not None or self.other_answer is not None
        else:
            return self.user_answer is not None
