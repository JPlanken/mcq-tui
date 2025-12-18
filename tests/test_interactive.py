#!/usr/bin/env python3
"""
Interactive test script for MCQ TUI
Simulates user interactions using pexpect
"""

import sys
import pexpect
from pathlib import Path

def test_basic_flow():
    """Test basic question answering flow"""
    script_path = Path(__file__).parent.parent / "mcq_tui.py"
    example_path = Path(__file__).parent.parent / "example_questions.yaml"
    
    if not example_path.exists():
        print("❌ Example questions file not found")
        return False
    
    print("Starting interactive test...")
    print(f"Script: {script_path}")
    print(f"Questions: {example_path}")
    print()
    
    try:
        # Start the TUI
        child = pexpect.spawn(
            f"python3 {script_path} {example_path}",
            encoding='utf-8',
            timeout=10
        )
        child.logfile = sys.stdout  # Show output
        
        # Wait for question to appear
        print("Waiting for question display...")
        child.expect("Question", timeout=5)
        print("✓ Question displayed")
        
        # Answer first question (single-select)
        print("\nAnswering first question (single-select) with '2'...")
        child.send('2')
        child.expect("✓", timeout=2)  # Checkmark should appear
        print("✓ Selection confirmed")
        
        # Press Enter to confirm and move to next
        print("\nPressing Enter to confirm...")
        child.send('\r')
        child.expect("Question", timeout=3)
        print("✓ Moved to next question")
        
        # Test multi-select
        print("\nTesting multi-select question...")
        child.expect("multi-select", timeout=3)
        print("✓ Multi-select question detected")
        
        # Select option 1
        print("\nSelecting option 1...")
        child.send('1')
        child.expect("✓", timeout=2)
        print("✓ Option 1 selected")
        
        # Select option 3
        print("\nSelecting option 3...")
        child.send('3')
        child.expect("✓", timeout=2)
        print("✓ Option 3 selected")
        
        # Press Enter to confirm
        print("\nPressing Enter to confirm selections...")
        child.send('\r')
        child.expect("Question", timeout=3)
        print("✓ Multi-select confirmed")
        
        # Test navigation - go back
        print("\nTesting navigation - going back...")
        child.send('\x1b[D')  # Left arrow
        child.expect("Question", timeout=3)
        print("✓ Navigated back")
        
        # Test jump command
        print("\nTesting jump command...")
        child.send('j')
        child.expect("Jump to question", timeout=3)
        print("✓ Jump prompt appeared")
        child.send('3\r')  # Jump to question 3
        child.expect("Question", timeout=3)
        print("✓ Jumped to question 3")
        
        # Test summary command
        print("\nTesting summary command...")
        child.send('s')
        child.expect("Summary", timeout=3)
        print("✓ Summary displayed")
        child.send('\r')  # Return to questions
        child.expect("Question", timeout=3)
        print("✓ Returned to questions")
        
        # Quit
        print("\nQuitting...")
        child.send('q')
        child.expect("Quit quiz", timeout=3)
        child.send('\r')  # Confirm quit
        child.expect(pexpect.EOF, timeout=3)
        print("✓ Quit successfully")
        
        print("\n" + "="*60)
        print("✅ All interactive tests passed!")
        print("="*60)
        return True
        
    except pexpect.TIMEOUT as e:
        print(f"\n❌ Test timed out: {e}")
        print(f"Last output: {child.before if 'child' in locals() else 'N/A'}")
        return False
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quick_quit():
    """Test that quit works immediately"""
    script_path = Path(__file__).parent.parent / "mcq_tui.py"
    example_path = Path(__file__).parent.parent / "example_questions.yaml"
    
    try:
        child = pexpect.spawn(
            f"python3 {script_path} {example_path}",
            encoding='utf-8',
            timeout=5
        )
        
        child.expect("Question", timeout=3)
        child.send('q')
        child.expect("Quit quiz", timeout=2)
        child.send('\r')
        child.expect(pexpect.EOF, timeout=2)
        
        print("✓ Quick quit test passed")
        return True
    except Exception as e:
        print(f"❌ Quick quit test failed: {e}")
        return False


if __name__ == '__main__':
    try:
        import pexpect
    except ImportError:
        print("❌ pexpect not installed")
        print("Install with: pip install pexpect")
        print("\nAlternatively, run unit tests: python3 test_mcq_tui.py")
        sys.exit(1)
    
    print("="*60)
    print("MCQ TUI Interactive Test Suite")
    print("="*60)
    print()
    
    # Run quick quit test first
    print("Test 1: Quick Quit")
    print("-" * 60)
    test1 = test_quick_quit()
    print()
    
    # Run full flow test
    print("Test 2: Full Flow")
    print("-" * 60)
    test2 = test_basic_flow()
    print()
    
    # Summary
    if test1 and test2:
        print("="*60)
        print("✅ All tests passed!")
        print("="*60)
        sys.exit(0)
    else:
        print("="*60)
        print("❌ Some tests failed")
        print("="*60)
        sys.exit(1)
