# Multiple Choice Question TUI

A Rich-based terminal user interface for answering multiple choice questions from YAML files with interactive visual feedback.

## Quick Start

```bash
# Install
cd mcq-tui
uv pip install -e .

# Run
mcq example_questions.yaml
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions and troubleshooting.

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
- Press number key (1-N) to select, then Enter to confirm
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
- Press Enter to confirm

## YAML Format

The TUI expects YAML files with questions in the following format:

```yaml
title: "Sample Quiz"
description: "A quiz about programming"
author: "John Doe"

questions:
  # Single-select (default)
  - id: 1
    question: "What is the capital of France?"
    type: single
    options:
      - "London"
      - "Paris"
      - "Berlin"
      - "Madrid"
  
  # Multi-select
  - id: 2
    question: "Which programming languages do you know? (Select all that apply)"
    type: multi
    options:
      - "Python"
      - "JavaScript"
      - "Rust"
      - "Go"
  
  # Yes/No
  - id: 3
    question: "Do you prefer Python over JavaScript?"
    type: yesno
```

After answering questions, the YAML file will be updated with answers:

```yaml
questions:
  - id: 1
    question: "What is the capital of France?"
    type: single
    options:
      - "London"
      - "Paris"
      - "Berlin"
      - "Madrid"
    answer:
      index: 2
      option: "Paris"
metadata:
  last_answered: "2025-12-18T10:36:27.096193"
  answered_count: 1
  total_questions: 3
```

**Format Rules:**
- Root level: `title`, `description`, `author` (all optional)
- `questions` array contains question objects
- Each question has:
  - `id` (optional): Unique identifier for the question (string or number)
  - `question` (required): The question text
  - `type` (optional): `single`, `multi`, or `yesno` (defaults to `single`)
  - `options` (required for `single` and `multi`, optional for `yesno`): Array of option strings
- Options are displayed as numbered choices (1, 2, 3...)
- Option 0 is always "Other" for single-select questions

**Answer Storage:**
- Answers are automatically saved back to the YAML file when you finish or exit
- Each answered question gets an `answer` field with the selected response
- A `metadata` section is added with timestamp and statistics
- Answers persist in the same file, making it easy to share results with agents or review later

## Features

- ✅ **Multiple Question Types**: Single-select, multi-select, and yes/no
- ✅ **Interactive Visual Feedback**: Immediate checkmarks and highlighting when selecting options
- ✅ **Number Key Navigation**: Press number keys (1, 2, 3...) for fast selection
- ✅ **Arrow Key Navigation**: ← previous, → next question
- ✅ **Keyboard Shortcuts**: `j` (jump), `s` (summary), `q` (quit)
- ✅ **Progress Tracking**: Shows current question number and answer status
- ✅ **Final Summary**: Review all answers at the end
- ✅ **Automatic Answer Storage**: Answers are automatically saved back to the YAML file
- ✅ **Question IDs**: Support for question IDs to track answers across sessions
- ✅ **Ctrl+C Support**: Quit anytime with Ctrl+C (saves partial results)
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
├── src/                      # Main package
│   ├── __init__.py           # Package exports
│   ├── question.py           # Question data model
│   ├── parser.py             # YAML parsing
│   ├── display.py            # Display functions
│   ├── input_handlers.py     # Input handling
│   ├── export.py             # Answer export functionality
│   ├── constants.py          # Constants and enums
│   ├── console.py            # Shared console instance
│   ├── terminal.py           # Terminal management utilities
│   ├── navigation.py         # Navigation utilities
│   └── answer_formatting.py  # Answer formatting utilities
├── mcq_tui.py                # Main CLI entry point
├── tests/                    # Test suite
│   ├── test_mcq_tui.py      # Unit tests
│   ├── test_simple.py        # Simple validation tests
│   ├── test_utilities.py     # Utility function tests
│   ├── test_interactive.py   # Interactive tests (requires pexpect)
│   └── TESTING.md            # Testing documentation
├── example_questions.yaml    # Sample questions
├── pyproject.toml            # Project configuration
├── INSTALL.md                # Installation guide
├── CONTEXT.md                # Technical details
└── README.md                 # This file
```

## Testing

Run the test suite to verify everything works:

```bash
# Simple tests (no extra dependencies)
python3 tests/test_simple.py

# Unit tests
python3 tests/test_mcq_tui.py

# Utility tests
python3 tests/test_utilities.py

# Interactive tests (requires pexpect: pip install pexpect)
python3 tests/test_interactive.py
```

See `tests/TESTING.md` for detailed testing documentation.

## Requirements

- Python 3.8+
- `rich` >= 13.0.0
- `pyyaml` >= 6.0

## Documentation

- **[INSTALL.md](INSTALL.md)**: Detailed installation guide and troubleshooting
- **[CONTEXT.md](CONTEXT.md)**: Technical implementation details and architecture
- **[tests/TESTING.md](tests/TESTING.md)**: Testing documentation

## License

MIT License
