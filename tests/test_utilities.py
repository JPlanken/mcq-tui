#!/usr/bin/env python3
"""
Test suite for utility functions
Tests the new utility modules without requiring interactive input
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import (
    Question, QuestionType, NavCommand,
    format_navigation_hints, handle_navigation_command,
    format_yesno_answer, format_single_answer, format_multi_answer,
    get_answer_display_text, get_answer_summary_text,
)


class TestConstants(unittest.TestCase):
    """Test constants and enums"""
    
    def test_question_type_values(self):
        """Test QuestionType enum values"""
        self.assertEqual(QuestionType.SINGLE, "single")
        self.assertEqual(QuestionType.MULTI, "multi")
        self.assertEqual(QuestionType.YESNO, "yesno")
    
    def test_nav_command_values(self):
        """Test NavCommand enum values"""
        self.assertEqual(NavCommand.QUIT, "q")
        self.assertEqual(NavCommand.JUMP, "j")
        self.assertEqual(NavCommand.SUMMARY, "s")
        self.assertEqual(NavCommand.PREVIOUS, "p")
        self.assertEqual(NavCommand.NEXT, "n")


class TestNavigationUtilities(unittest.TestCase):
    """Test navigation utility functions"""
    
    def test_format_navigation_hints_first_question(self):
        """Test navigation hints for first question"""
        hints = format_navigation_hints(1, 5)
        self.assertIn("→ = next", hints)
        self.assertIn("'j' = jump", hints)
        self.assertIn("'s' = summary", hints)
        self.assertIn("'q' = quit", hints)
        self.assertNotIn("← = previous", hints)
    
    def test_format_navigation_hints_middle_question(self):
        """Test navigation hints for middle question"""
        hints = format_navigation_hints(3, 5)
        self.assertIn("← = previous", hints)
        self.assertIn("→ = next", hints)
        self.assertIn("'j' = jump", hints)
        self.assertIn("'s' = summary", hints)
        self.assertIn("'q' = quit", hints)
    
    def test_format_navigation_hints_last_question(self):
        """Test navigation hints for last question"""
        hints = format_navigation_hints(5, 5)
        self.assertIn("← = previous", hints)
        self.assertNotIn("→ = next", hints)
        self.assertIn("'j' = jump", hints)
        self.assertIn("'s' = summary", hints)
        self.assertIn("'q' = quit", hints)
    
    def test_handle_navigation_command_quit(self):
        """Test handling quit command"""
        result = handle_navigation_command('q')
        self.assertEqual(result, NavCommand.QUIT)
    
    def test_handle_navigation_command_jump(self):
        """Test handling jump command"""
        result = handle_navigation_command('j')
        self.assertEqual(result, NavCommand.JUMP)
    
    def test_handle_navigation_command_summary(self):
        """Test handling summary command"""
        result = handle_navigation_command('s')
        self.assertEqual(result, NavCommand.SUMMARY)
    
    def test_handle_navigation_command_enter(self):
        """Test handling Enter key"""
        result = handle_navigation_command('\r')
        self.assertEqual(result, NavCommand.NEXT)
        result = handle_navigation_command('\n')
        self.assertEqual(result, NavCommand.NEXT)
    
    def test_handle_navigation_command_invalid(self):
        """Test handling invalid command"""
        result = handle_navigation_command('x')
        self.assertIsNone(result)


class TestAnswerFormatting(unittest.TestCase):
    """Test answer formatting utilities"""
    
    def test_format_yesno_answer_yes(self):
        """Test formatting yes answer"""
        q = Question("Test?", [], QuestionType.YESNO)
        q.user_answer = 1
        answer, other = format_yesno_answer(q)
        self.assertEqual(answer, "1")
        self.assertIsNone(other)
    
    def test_format_yesno_answer_no(self):
        """Test formatting no answer"""
        q = Question("Test?", [], QuestionType.YESNO)
        q.user_answer = 2
        answer, other = format_yesno_answer(q)
        self.assertEqual(answer, "2")
        self.assertIsNone(other)
    
    def test_format_yesno_answer_other(self):
        """Test formatting other answer"""
        q = Question("Test?", [], QuestionType.YESNO)
        q.user_answer = 3
        q.other_answer = "Maybe"
        answer, other = format_yesno_answer(q)
        self.assertEqual(answer, "3:Maybe")
        self.assertEqual(other, "Maybe")
    
    def test_format_yesno_answer_unanswered(self):
        """Test formatting unanswered yes/no"""
        q = Question("Test?", [], QuestionType.YESNO)
        answer, other = format_yesno_answer(q)
        self.assertIsNone(answer)
        self.assertIsNone(other)
    
    def test_format_single_answer(self):
        """Test formatting single-select answer"""
        q = Question("Test?", ["A", "B"], QuestionType.SINGLE)
        q.user_answer = 2
        answer, other = format_single_answer(q)
        self.assertEqual(answer, "2")
        self.assertIsNone(other)
    
    def test_format_single_answer_other(self):
        """Test formatting single-select other answer"""
        q = Question("Test?", ["A", "B"], QuestionType.SINGLE)
        q.user_answer = 0
        q.other_answer = "Custom"
        answer, other = format_single_answer(q)
        self.assertEqual(answer, "0:Custom")
        self.assertEqual(other, "Custom")
    
    def test_format_single_answer_unanswered(self):
        """Test formatting unanswered single-select"""
        q = Question("Test?", ["A", "B"], QuestionType.SINGLE)
        answer, other = format_single_answer(q)
        self.assertIsNone(answer)
        self.assertIsNone(other)
    
    def test_format_multi_answer(self):
        """Test formatting multi-select answer"""
        q = Question("Test?", ["A", "B", "C"], QuestionType.MULTI)
        q.user_answers = [1, 3]
        answer = format_multi_answer(q)
        self.assertEqual(answer, "1,3")
    
    def test_format_multi_answer_empty(self):
        """Test formatting empty multi-select answer"""
        q = Question("Test?", ["A", "B"], QuestionType.MULTI)
        answer = format_multi_answer(q)
        self.assertIsNone(answer)
    
    def test_format_multi_answer_sorted(self):
        """Test that multi-select answers are sorted"""
        q = Question("Test?", ["A", "B", "C"], QuestionType.MULTI)
        q.user_answers = [3, 1, 2]
        answer = format_multi_answer(q)
        self.assertEqual(answer, "1,2,3")


class TestAnswerDisplayText(unittest.TestCase):
    """Test answer display text formatting"""
    
    def test_get_answer_display_text_single(self):
        """Test display text for single-select"""
        q = Question("Test?", ["A", "B"], QuestionType.SINGLE)
        q.user_answer = 1
        text = get_answer_display_text(q)
        self.assertIn("Option 1", text)
        self.assertIn("A", text)
    
    def test_get_answer_display_text_single_other(self):
        """Test display text for single-select other"""
        q = Question("Test?", ["A", "B"], QuestionType.SINGLE)
        q.user_answer = 0
        q.other_answer = "Custom"
        text = get_answer_display_text(q)
        self.assertIn("Other", text)
        self.assertIn("Custom", text)
    
    def test_get_answer_display_text_multi(self):
        """Test display text for multi-select"""
        q = Question("Test?", ["A", "B", "C"], QuestionType.MULTI)
        q.user_answers = [1, 3]
        text = get_answer_display_text(q)
        self.assertIn("Option 1", text)
        self.assertIn("Option 3", text)
        self.assertIn("A", text)
        self.assertIn("C", text)
    
    def test_get_answer_display_text_yesno(self):
        """Test display text for yes/no"""
        q = Question("Test?", [], QuestionType.YESNO)
        q.user_answer = 1
        text = get_answer_display_text(q)
        self.assertIn("Yes", text)
        self.assertIn("1", text)
    
    def test_get_answer_display_text_unanswered(self):
        """Test display text for unanswered question"""
        q = Question("Test?", ["A", "B"], QuestionType.SINGLE)
        text = get_answer_display_text(q)
        self.assertIn("No answer", text)
    
    def test_get_answer_summary_text_single(self):
        """Test summary text for single-select"""
        q = Question("Test?", ["A", "B"], QuestionType.SINGLE)
        q.user_answer = 1
        text = get_answer_summary_text(q)
        self.assertEqual(text, "Option 1: A")
    
    def test_get_answer_summary_text_multi(self):
        """Test summary text for multi-select"""
        q = Question("Test?", ["A", "B", "C"], QuestionType.MULTI)
        q.user_answers = [1, 3]
        text = get_answer_summary_text(q)
        self.assertIn("1: A", text)
        self.assertIn("3: C", text)
    
    def test_get_answer_summary_text_yesno(self):
        """Test summary text for yes/no"""
        q = Question("Test?", [], QuestionType.YESNO)
        q.user_answer = 1
        text = get_answer_summary_text(q)
        self.assertEqual(text, "Yes (1)")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""
    
    def test_format_navigation_hints_single_question(self):
        """Test navigation hints for single question"""
        hints = format_navigation_hints(1, 1)
        self.assertNotIn("← = previous", hints)
        self.assertNotIn("→ = next", hints)
    
    def test_format_multi_answer_empty_list(self):
        """Test formatting with empty user_answers list"""
        q = Question("Test?", ["A", "B"], QuestionType.MULTI)
        q.user_answers = []
        answer = format_multi_answer(q)
        self.assertIsNone(answer)
    
    def test_get_answer_display_text_multi_empty(self):
        """Test display text for multi-select with no answers"""
        q = Question("Test?", ["A", "B"], QuestionType.MULTI)
        text = get_answer_display_text(q)
        self.assertIn("No answers", text)
    
    def test_format_yesno_answer_legacy_string(self):
        """Test formatting yes/no with legacy string values"""
        q = Question("Test?", [], QuestionType.YESNO)
        q.user_answer = "y"
        answer, other = format_yesno_answer(q)
        self.assertEqual(answer, "1")
        
        q.user_answer = "n"
        answer, other = format_yesno_answer(q)
        self.assertEqual(answer, "2")


if __name__ == '__main__':
    unittest.main(verbosity=2)
