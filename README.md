# Multiple Choice Question TUI

A Rich-based terminal user interface for answering multiple choice questions from YAML files.

## Installation

### Install as CLI Tool

```bash
uv pip install -e .
```

That's it! The `mcq` command should be available. If not found, ensure `~/.local/bin` is in your PATH (usually is by default).

**Usage:**
```bash
mcq questions.yaml
mcq --help
```

### Development Installation (Recommended)

```bash
uv sync
uv run mcq questions.yaml
```

This creates a virtual environment and installs dependencies. Use `uv run` to execute commands.

## Usage

### As CLI Tool

```bash
mcq questions.yaml
mcq --help
```

### As Python Script

```bash
python mcq_tui.py questions.yaml
```

### Example

```bash
mcq example_questions.yaml
```

## YAML Format

The TUI expects YAML files with questions in the following format:

```yaml
title: "Sample Quiz"
description: "A quiz about programming"
author: "John Doe"

questions:
  - question: "What is the capital of France?"
    options:
      - "London"
      - "Paris"
      - "Berlin"
      - "Madrid"
  
  - question: "Which programming language is known for data science?"
    options:
      - "Java"
      - "C++"
      - "Python"
      - "JavaScript"
```

**Format Rules:**
- Root level: `title`, `description`, `author` (all optional)
- `questions` array contains question objects
- Each question has: `question` (text), `options` (array of strings)
- Options are displayed as numbered choices (1, 2, 3...)
- Option 0 is always "Other" for free text input

## Features

- ✅ YAML format support
- ✅ Interactive question-by-question answering
- ✅ Arrow key navigation (← previous, → next)
- ✅ Numbered options (1, 2, 3...)
- ✅ "Other" option (0) for free text input
- ✅ Jump to any question (`j` command)
- ✅ Progress tracking
- ✅ Final summary with all answers
- ✅ Beautiful Rich-based terminal UI

## Navigation

- **→** or **Enter** = Next question
- **←** = Previous question
- **j** = Jump to specific question number
- **s** = Show summary
- **q** = Quit

## Files

- `mcq_tui.py` - Main TUI application
- `example_questions.yaml` - Sample YAML questions
- `pyproject.toml` - Project configuration and dependencies
- `INSTALL.md` - Installation guide
