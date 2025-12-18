"""
Question data model
"""

from typing import List, Optional


class Question:
    """Represents a question with different types"""
    
    def __init__(self, question_text: str, options: List[str], question_type: str = "single"):
        self.question_text = question_text.strip()
        self.options = [opt.strip() for opt in options]
        self.question_type = question_type.lower()  # "single", "multi", "yesno"
        
        # For single-select: user_answer is int (1-N) or 0 for "Other"
        # For multi-select: user_answers is List[int] (can be empty)
        # For yesno: user_answer is "y", "n", or "other" (with other_answer)
        self.user_answer: Optional[int] = None  # Single-select answer
        self.user_answers: List[int] = []  # Multi-select answers
        self.other_answer: Optional[str] = None  # Free text if user chose "Other"
    
    def is_answered(self) -> bool:
        """Check if question has been answered"""
        if self.question_type == "multi":
            return len(self.user_answers) > 0
        elif self.question_type == "yesno":
            return self.user_answer is not None or self.other_answer is not None
        else:  # single
            return self.user_answer is not None
