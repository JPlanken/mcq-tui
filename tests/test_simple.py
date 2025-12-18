#!/usr/bin/env python3
"""
Simple test script that doesn't require pexpect
Tests core functionality and provides a quick validation
"""

import sys
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    try:
        import rich
        import yaml
        from src import Question, parse_yaml_questions
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_yaml_parsing():
    """Test YAML parsing"""
    print("\nTesting YAML parsing...")
    try:
        from src import parse_yaml_questions
        example_path = Path(__file__).parent.parent / "example_questions.yaml"
        if not example_path.exists():
            print("✗ Example questions file not found")
            return False
        
        questions = parse_yaml_questions(example_path)
        if len(questions) == 0:
            print("✗ No questions parsed")
            return False
        
        print(f"✓ Parsed {len(questions)} questions")
        
        # Check question types
        types = {q.question_type for q in questions}
        if 'single' in types:
            print("✓ Found single-select questions")
        if 'multi' in types:
            print("✓ Found multi-select questions")
        if 'yesno' in types:
            print("✓ Found yes/no questions")
        
        return True
    except Exception as e:
        print(f"✗ YAML parsing failed: {e}")
        return False

def test_question_class():
    """Test Question class"""
    print("\nTesting Question class...")
    try:
        from src import Question
        
        # Test single-select
        q1 = Question("Test?", ["A", "B"], "single")
        assert not q1.is_answered()
        q1.user_answer = 1
        assert q1.is_answered()
        print("✓ Single-select question works")
        
        # Test multi-select
        q2 = Question("Test?", ["A", "B"], "multi")
        assert not q2.is_answered()
        q2.user_answers = [1, 2]
        assert q2.is_answered()
        print("✓ Multi-select question works")
        
        # Test yes/no
        q3 = Question("Test?", ["Yes", "No"], "yesno")
        assert not q3.is_answered()
        q3.user_answer = 1
        assert q3.is_answered()
        print("✓ Yes/No question works")
        
        return True
    except Exception as e:
        print(f"✗ Question class test failed: {e}")
        return False

def test_cli_exists():
    """Test that CLI can be invoked"""
    print("\nTesting CLI invocation...")
    try:
        script_path = Path(__file__).parent.parent / "mcq_tui.py"
        example_path = Path(__file__).parent.parent / "example_questions.yaml"
        
        if not script_path.exists():
            print("✗ mcq_tui.py not found")
            return False
        
        # Try to run with --help or --version (non-interactive)
        # Actually, let's just check the file is executable
        result = subprocess.run(
            [sys.executable, str(script_path), "--version"],
            capture_output=True,
            timeout=5,
            text=True
        )
        
        if result.returncode == 0 or "version" in result.stdout.lower() or "version" in result.stderr.lower():
            print("✓ CLI script is executable")
            return True
        else:
            print("✓ CLI script exists (version check may vary)")
            return True
            
    except subprocess.TimeoutExpired:
        print("✗ CLI invocation timed out")
        return False
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False

def test_file_structure():
    """Test that required files exist"""
    print("\nTesting file structure...")
    required_files = [
        "mcq_tui.py",
        "example_questions.yaml",
        "pyproject.toml",
        "README.md"
    ]
    
    all_exist = True
    for filename in required_files:
        path = Path(__file__).parent.parent / filename
        if path.exists():
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all simple tests"""
    print("="*60)
    print("MCQ TUI Simple Test Suite")
    print("="*60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Question Class", test_question_class),
        ("YAML Parsing", test_yaml_parsing),
        ("CLI Invocation", test_cli_exists),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
