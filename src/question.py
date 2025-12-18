"""
Question data model
"""

from typing import List, Optional, Dict, Any

from .constants import QuestionType


class Question:
    """Represents a question with different types"""
    
    def __init__(self, question_text: str, options: List[str], question_type: str = QuestionType.SINGLE, question_id: Optional[str] = None):
        self.question_text = question_text.strip()
        self.options = [opt.strip() for opt in options]
        self.question_type = question_type.lower()
        self.question_id = question_id
        
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
    
    def get_answer_dict(self) -> Dict[str, Any]:
        """
        Get the answer in a structured, serializable format for sharing with agents.
        
        Returns:
            Dictionary containing question id, type, and answer data
        """
        result: Dict[str, Any] = {
            "id": self.question_id,
            "question": self.question_text,
            "type": self.question_type,
        }
        
        if self.question_type == QuestionType.MULTI:
            if self.user_answers:
                result["answer"] = {
                    "selected_indices": sorted(self.user_answers),
                    "selected_options": [self.options[i - 1] for i in sorted(self.user_answers)],
                }
            else:
                result["answer"] = None
        elif self.question_type == QuestionType.YESNO:
            if self.user_answer == 1:
                result["answer"] = "Yes"
            elif self.user_answer == 2:
                result["answer"] = "No"
            elif self.user_answer == 3 and self.other_answer:
                result["answer"] = {
                    "type": "Other",
                    "value": self.other_answer
                }
            else:
                result["answer"] = None
        else:  # single select
            if self.user_answer == 0 and self.other_answer:
                result["answer"] = {
                    "type": "Other",
                    "value": self.other_answer
                }
            elif self.user_answer is not None:
                result["answer"] = {
                    "index": self.user_answer,
                    "option": self.options[self.user_answer - 1]
                }
            else:
                result["answer"] = None
        
        return result
