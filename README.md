# Multiple Choice Question TUI

A Rich-based terminal user interface for answering multiple choice questions from YAML files with interactive visual feedback.

## Installation

### Install as CLI Tool

```bash
cd mcq-tui
uv pip install -e .
```

The `mcq` command should now be available. If not found, ensure `~/.local/bin` is in your PATH.

**Usage:**
```bash
mcq questions.yaml
mcq --help
mcq --version
```

### Development Installation

```bash
cd mcq-tui
uv sync
uv run mcq questions.yaml
```

This creates a virtual environment and installs dependencies. Use `uv run` to execute commands.

## Usage

### Basic Usage

```bash
mcq questions.yaml
```

If no file is provided, you'll be prompted to enter the path.

### Example

```bash
mcq example_questions.yaml
```

## Question Types

The TUI supports three question types:

### 1. Single-Select (`type: single` or default)
- Choose one option from a list
- Press number key (1-N) to select
- Option 0 for "Other" (free text input)

### 2. Multi-Select (`type: multi`)
- Select multiple options
- Press number keys (1-N) to toggle selections
- Visual checkmarks show selected options
- Press Enter to confirm

### 3. Yes/No (`type: yesno`)
- Simple Yes/No/Other questions
- Press `1` (Yes), `2` (No), or `3` (Other)
- Also accepts `y`, `n`, `o` for compatibility

## YAML Format

The TUI expects YAML files with questions in the following format:

```yaml
title: "Sample Quiz"
description: "A quiz about programming"
author: "John Doe"

questions:
  # Single-select (default)
  - question: "What is the capital of France?"
    type: single
    options:
      - "London"
      - "Paris"
      - "Berlin"
      - "Madrid"
  
  # Multi-select
  - question: "Which programming languages do you know? (Select all that apply)"
    type: multi
    options:
      - "Python"
      - "JavaScript"
      - "Rust"
      - "Go"
  
  # Yes/No
  - question: "Do you prefer Python over JavaScript?"
    type: yesno
```

**Format Rules:**
- Root level: `title`, `description`, `author` (all optional)
- `questions` array contains question objects
- Each question has:
  - `question` (required): The question text
  - `type` (optional): `single`, `multi`, or `yesno` (defaults to `single`)
  - `options` (required for `single` and `multi`, optional for `yesno`): Array of option strings
- Options are displayed as numbered choices (1, 2, 3...)
- Option 0 is always "Other" for single-select questions

## Features

- ✅ **Multiple Question Types**: Single-select, multi-select, and yes/no
- ✅ **Interactive Visual Feedback**: Immediate checkmarks and highlighting when selecting options
- ✅ **Number Key Navigation**: Press number keys (1, 2, 3...) for fast selection
- ✅ **Arrow Key Navigation**: ← previous, → next question
- ✅ **Keyboard Shortcuts**: `j` (jump), `s` (summary), `q` (quit)
- ✅ **Progress Tracking**: Shows current question number and answer status
- ✅ **Final Summary**: Review all answers at the end
- ✅ **Ctrl+C Support**: Quit anytime with Ctrl+C
- ✅ **Beautiful Rich-based Terminal UI**: Colorful, formatted display
- ✅ **YAML Format Support**: Easy-to-edit question files

## Navigation

### During Questions

- **Number keys (1-N)**: Select/toggle options (immediate visual feedback)
- **Enter**: Confirm selection and move to next question
- **→** or **Enter**: Next question
- **←**: Previous question
- **j**: Jump to specific question number
- **s**: Show summary of all answers
- **q**: Quit quiz
- **Ctrl+C**: Quit anytime

### Visual Feedback

- **Selected options**: Bold green with checkmark (✓)
- **Unselected options**: Dimmed text
- **Question type**: Shown in panel subtitle
- **Answer status**: Shown in header (✓ Answered / ○ Not answered)


## Project Structure

```
mcq-tui/
├── src/                 # Main package
│   ├── __init__.py      # Package exports
│   ├── question.py      # Question data model
│   ├── parser.py        # YAML parsing
│   ├── display.py       # Display functions
│   └── input_handlers.py # Input handling
├── mcq_tui.py           # Main CLI entry point
├── tests/               # Test suite
│   ├── test_mcq_tui.py  # Unit tests
│   ├── test_simple.py   # Simple validation tests
│   ├── test_interactive.py # Interactive tests (requires pexpect)
│   └── TESTING.md       # Testing documentation
├── example_questions.yaml # Sample questions
├── pyproject.toml       # Project configuration
├── INSTALL.md           # Installation guide
├── CONTEXT.md           # Technical details
└── README.md            # This file
```

## Testing

Run the test suite to verify everything works:

```bash
# Simple tests (no extra dependencies)
python3 tests/test_simple.py

# Unit tests
python3 tests/test_mcq_tui.py

# Interactive tests (requires pexpect: pip install pexpect)
python3 tests/test_interactive.py
```

See `tests/TESTING.md` for detailed testing documentation.

## Requirements

- Python 3.8+
- `rich` >= 13.0.0
- `pyyaml` >= 6.0

## License

MIT License
