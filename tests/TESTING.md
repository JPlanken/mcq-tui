# Testing the MCQ TUI

This document describes how to test the MCQ TUI application.

## Quick Test

Run the unit tests (no dependencies required beyond the main ones):

```bash
python3 test_mcq_tui.py
```

This will test:
- Question class functionality
- YAML parsing
- Display functions
- Utility functions (navigation, answer formatting)

## Interactive Testing

### Manual Testing

The best way to test the TUI is to run it manually:

```bash
python3 mcq_tui.py example_questions.yaml
```

Test scenarios:
1. **Single-select questions**: Press number keys (1-4), verify checkmark appears, press Enter
2. **Multi-select questions**: Press multiple number keys, verify multiple checkmarks, press Enter
3. **Yes/No questions**: Press 1 (Yes), 2 (No), or 3 (Other)
4. **Navigation**: 
   - Press `←` (left arrow) to go back
   - Press `→` (right arrow) to go forward
   - Press `j` to jump to a specific question
   - Press `s` to show summary
   - Press `q` to quit
5. **Other option**: Press `0` in single-select questions to enter free text
6. **Answer storage**: After completing questions, verify answers are saved to YAML file
7. **Ctrl+C**: Should quit cleanly at any time (saves partial results with confirmation)

### Automated Interactive Testing

For automated testing of the interactive TUI, install `pexpect`:

```bash
pip install pexpect
```

Then run:

```bash
python3 test_interactive.py
```

This will automatically:
- Start the TUI
- Answer questions
- Test navigation commands
- Test jump and summary features
- Verify quit functionality

## Test Files

- `test_simple.py` - Quick validation tests (no special dependencies)
- `test_mcq_tui.py` - Comprehensive unit tests (no special dependencies)
- `test_utilities.py` - Utility function tests (no special dependencies)
- `test_interactive.py` - Integration tests (requires pexpect)

## What Gets Tested

### Unit Tests (`test_mcq_tui.py`)

✅ Question class creation and answering  
✅ YAML parsing (all question types, including question IDs)  
✅ Default question type handling  
✅ Answer processing logic  
✅ Answer storage and serialization (`get_answer_dict()`)  
✅ Answer export to YAML  
✅ Display functions (non-crashing)  
✅ Summary generation  

### Integration Tests (`test_interactive.py`)

✅ TUI startup  
✅ Question display  
✅ Answer selection (single, multi, yes/no)  
✅ Navigation (arrows, jump, summary)  
✅ Quit functionality  

## Running Tests in CI/CD

For continuous integration, you can run:

```bash
# Unit tests only (fast, no dependencies)
python3 test_mcq_tui.py

# Or with unittest discovery
python3 -m unittest discover -s . -p "test_*.py"
```

## Expected Output

When tests pass, you should see:

```
Running Unit Tests
============================================================
test_single_select_question ... ok
test_multi_select_question ... ok
...
----------------------------------------------------------------------
Ran 12 tests in 0.009s

OK
```

## Troubleshooting

### Tests fail with "pexpect not available"

Install pexpect:
```bash
pip install pexpect
```

Or skip integration tests and run only unit tests:
```bash
python3 test_mcq_tui.py
```

### Tests fail with import errors

Make sure you're in the `mcq-tui` directory and dependencies are installed:
```bash
pip install rich pyyaml
```

### Interactive tests timeout

The interactive tests have a timeout. If your system is slow, you may need to increase the timeout values in `test_interactive.py`.
