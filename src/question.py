"""
Question data model
"""

from typing import List, Optional, Dict, Any

from .constants import QuestionType


class Question:
    """Represents a question with different types"""
    
    def __init__(self, question_text: str, options: List[str], question_type: str = QuestionType.SINGLE, question_id: Optional[str] = None, correct_answer: Optional[int] = None):
        # Validate and sanitize inputs
        if not question_text or not question_text.strip():
            raise ValueError("Question text cannot be empty")
        
        self.question_text = question_text.strip()
        self.options = [opt.strip() for opt in options] if options else []
        self.question_type = question_type.lower() if question_type else QuestionType.SINGLE
        self.question_id = question_id
        
        # Validate correct_answer is within bounds if provided
        if correct_answer is not None:
            if not isinstance(correct_answer, int) or correct_answer < 1 or correct_answer > len(self.options):
                self.correct_answer = None  # Silently ignore invalid correct_answer
            else:
                self.correct_answer = correct_answer
        else:
            self.correct_answer = None
        
        self.user_answer: Optional[int] = None
        self.user_answers: List[int] = []
        self.other_answer: Optional[str] = None
    
    def is_correct(self) -> Optional[bool]:
        """Check if the user's answer is correct. Returns None if not answered or no correct answer defined."""
        if self.correct_answer is None:
            return None
        if not self.is_answered():
            return None
        
        if self.question_type == QuestionType.SINGLE:
            return self.user_answer == self.correct_answer
        elif self.question_type == QuestionType.MULTI:
            # For multi-select, check if all selected answers are correct (simplified)
            return set(self.user_answers) == {self.correct_answer}
        elif self.question_type == QuestionType.YESNO:
            return self.user_answer == self.correct_answer
        
        return None
    
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
                # Filter to valid indices only to prevent IndexError
                valid_indices = [i for i in sorted(self.user_answers) if 1 <= i <= len(self.options)]
                if valid_indices:
                    result["answer"] = {
                        "selected_indices": valid_indices,
                        "selected_options": [self.options[i - 1] for i in valid_indices],
                    }
                else:
                    result["answer"] = None
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
            elif self.user_answer is not None and 1 <= self.user_answer <= len(self.options):
                result["answer"] = {
                    "index": self.user_answer,
                    "option": self.options[self.user_answer - 1]
                }
            else:
                result["answer"] = None
        
        return result
