#!/usr/bin/env python3
"""
Test suite for MCQ TUI
Tests core functionality and simulates user interactions
"""

import unittest
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import io

# Add parent directory to path to import src package
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import Question, parse_yaml_questions, display_question, show_summary


class TestQuestion(unittest.TestCase):
    """Test Question class functionality"""
    
    def test_single_select_question(self):
        """Test single-select question creation and answering"""
        q = Question("What is 2+2?", ["3", "4", "5"], "single")
        self.assertEqual(q.question_text, "What is 2+2?")
        self.assertEqual(len(q.options), 3)
        self.assertFalse(q.is_answered())
        
        q.user_answer = 2
        self.assertTrue(q.is_answered())
        self.assertEqual(q.user_answer, 2)
    
    def test_multi_select_question(self):
        """Test multi-select question creation and answering"""
        q = Question("Select languages", ["Python", "Java"], "multi")
        self.assertFalse(q.is_answered())
        
        q.user_answers = [1, 2]
        self.assertTrue(q.is_answered())
        self.assertEqual(len(q.user_answers), 2)
        
        q.user_answers = []
        self.assertFalse(q.is_answered())
    
    def test_yesno_question(self):
        """Test yes/no question creation and answering"""
        q = Question("Do you like Python?", ["Yes", "No"], "yesno")
        self.assertFalse(q.is_answered())
        
        q.user_answer = 1
        self.assertTrue(q.is_answered())
        
        q.user_answer = None
        q.other_answer = "Maybe"
        self.assertTrue(q.is_answered())
    
    def test_question_with_other_option(self):
        """Test question with 'Other' option"""
        q = Question("Favorite language?", ["Python", "Java"], "single")
        q.user_answer = 0
        q.other_answer = "Rust"
        self.assertTrue(q.is_answered())
        self.assertEqual(q.other_answer, "Rust")


class TestYAMLParsing(unittest.TestCase):
    """Test YAML parsing functionality"""
    
    def test_parse_valid_yaml(self):
        """Test parsing a valid YAML file"""
        yaml_content = """
questions:
  - question: "Test question?"
    type: single
    options:
      - "Option 1"
      - "Option 2"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            questions = parse_yaml_questions(Path(temp_path))
            self.assertEqual(len(questions), 1)
            self.assertEqual(questions[0].question_text, "Test question?")
            self.assertEqual(questions[0].question_type, "single")
            self.assertEqual(len(questions[0].options), 2)
        finally:
            os.unlink(temp_path)
    
    def test_parse_multi_select(self):
        """Test parsing multi-select question"""
        yaml_content = """
questions:
  - question: "Select all that apply"
    type: multi
    options:
      - "A"
      - "B"
      - "C"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            questions = parse_yaml_questions(Path(temp_path))
            self.assertEqual(len(questions), 1)
            self.assertEqual(questions[0].question_type, "multi")
        finally:
            os.unlink(temp_path)
    
    def test_parse_yesno_question(self):
        """Test parsing yes/no question"""
        yaml_content = """
questions:
  - question: "Do you like tests?"
    type: yesno
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            questions = parse_yaml_questions(Path(temp_path))
            self.assertEqual(len(questions), 1)
            self.assertEqual(questions[0].question_type, "yesno")
            # Yes/No questions should have default options
            self.assertEqual(len(questions[0].options), 2)
        finally:
            os.unlink(temp_path)
    
    def test_parse_default_type(self):
        """Test that questions default to single-select"""
        yaml_content = """
questions:
  - question: "No type specified"
    options:
      - "A"
      - "B"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            questions = parse_yaml_questions(Path(temp_path))
            self.assertEqual(len(questions), 1)
            self.assertEqual(questions[0].question_type, "single")
        finally:
            os.unlink(temp_path)
    
    def test_parse_empty_file(self):
        """Test parsing empty or invalid YAML"""
        yaml_content = "questions: []"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            questions = parse_yaml_questions(Path(temp_path))
            self.assertEqual(len(questions), 0)
        finally:
            os.unlink(temp_path)
    
    def test_parse_example_file(self):
        """Test parsing the example questions file"""
        example_path = Path(__file__).parent.parent / "example_questions.yaml"
        if example_path.exists():
            questions = parse_yaml_questions(example_path)
            self.assertGreater(len(questions), 0)
            # Verify we have different question types
            types = {q.question_type for q in questions}
            self.assertIn("single", types)
            self.assertIn("multi", types)
            self.assertIn("yesno", types)
    
    def test_parse_invalid_yaml(self):
        """Test parsing invalid YAML"""
        yaml_content = "invalid: yaml: content: ["
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            questions = parse_yaml_questions(Path(temp_path))
            # Should return empty list on error, not crash
            self.assertEqual(len(questions), 0)
        finally:
            os.unlink(temp_path)
    
    def test_parse_missing_file(self):
        """Test parsing non-existent file"""
        fake_path = Path("/nonexistent/path/questions.yaml")
        questions = parse_yaml_questions(fake_path)
        # Should return empty list on error, not crash
        self.assertEqual(len(questions), 0)
    
    def test_parse_question_without_text(self):
        """Test parsing question without text"""
        yaml_content = """
questions:
  - type: single
    options:
      - "A"
      - "B"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            questions = parse_yaml_questions(Path(temp_path))
            # Questions without text should be skipped
            self.assertEqual(len(questions), 0)
        finally:
            os.unlink(temp_path)
    
    def test_parse_single_without_options(self):
        """Test parsing single-select without options"""
        yaml_content = """
questions:
  - question: "Test?"
    type: single
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            questions = parse_yaml_questions(Path(temp_path))
            # Single-select without options should be skipped
            self.assertEqual(len(questions), 0)
        finally:
            os.unlink(temp_path)


class TestDisplayFunctions(unittest.TestCase):
    """Test display functions (non-interactive parts)"""
    
    def test_display_question_single(self):
        """Test displaying a single-select question"""
        q = Question("Test?", ["A", "B"], "single")
        q.user_answer = 1
        
        # Capture output
        from rich.console import Console
        console = Console(file=io.StringIO(), width=80)
        
        # This should not raise an exception
        # We can't easily test the output format, but we can test it doesn't crash
        try:
            display_question(q, 1, 1)
        except Exception as e:
            self.fail(f"display_question raised {e}")
    
    def test_show_summary(self):
        """Test summary display"""
        questions = [
            Question("Q1?", ["A", "B"], "single"),
            Question("Q2?", ["X", "Y"], "multi"),
        ]
        questions[0].user_answer = 1
        questions[1].user_answers = [1, 2]
        
        # Should not raise an exception
        try:
            show_summary(questions)
        except Exception as e:
            self.fail(f"show_summary raised {e}")


def run_integration_test():
    """Run integration test using pexpect if available"""
    try:
        import pexpect
    except ImportError:
        print("pexpect not available, skipping integration tests")
        print("Install with: pip install pexpect")
        return False
    
    print("\n" + "="*60)
    print("Running Integration Test (requires pexpect)")
    print("="*60)
    
    script_path = Path(__file__).parent / "mcq_tui.py"
    example_path = Path(__file__).parent / "example_questions.yaml"
    
    if not example_path.exists():
        print("Example questions file not found, skipping integration test")
        return False
    
    try:
        # Start the TUI
        child = pexpect.spawn(
            f"python3 {script_path} {example_path}",
            encoding='utf-8',
            timeout=5
        )
        
        # Look for the question display
        child.expect("Question", timeout=3)
        print("✓ TUI started successfully")
        
        # Try to quit immediately
        child.send('q')
        child.expect("Quit quiz", timeout=2)
        child.send('\n')  # Confirm quit
        
        child.expect(pexpect.EOF, timeout=2)
        print("✓ Quit command works")
        
        return True
    except pexpect.TIMEOUT:
        print("✗ Integration test timed out")
        return False
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False


if __name__ == '__main__':
    # Run unit tests
    print("Running Unit Tests")
    print("="*60)
    unittest.main(verbosity=2, exit=False)
    
    # Run integration test if pexpect is available
    run_integration_test()
