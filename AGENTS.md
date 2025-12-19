# MCQ-TUI Agent Guide

Context for AI agents and developers working on this codebase.

## Entry Points

| Task | File | Function |
|------|------|----------|
| CLI entry | `mcq_tui.py` | `main()` |
| Question model | `src/question.py` | `Question` class |
| YAML parsing | `src/parser.py` | `parse_yaml_questions()` |
| Display | `src/display.py` | `display_question()`, `show_summary()` |
| Input | `src/input_handlers.py` | `get_user_answer()` |
| Export | `src/export.py` | `export_results_to_yaml()` |

## Module Map

```
mcq_tui.py              # CLI + main loop
src/
├── question.py         # Question dataclass, answer storage
├── parser.py           # YAML → Question[] parsing
├── display.py          # Rich-based rendering
├── input_handlers.py   # Raw terminal input per question type
├── export.py           # Save answers back to YAML
├── constants.py        # QuestionType, NavCommand enums
├── console.py          # Shared Rich Console instance
├── terminal.py         # raw_terminal() context manager
├── navigation.py       # Arrow keys, nav command handling
└── answer_formatting.py # Answer display text formatters
```

## Common Tasks

| Task | Files to modify |
|------|-----------------|
| Add question type | `constants.py` → `input_handlers.py` → `display.py` → `parser.py` |
| Modify input | `input_handlers.py`, `terminal.py` |
| Change display | `display.py`, `answer_formatting.py` |
| Add CLI option | `mcq_tui.py` (argparse section) |

## Question Types & Answer Storage

| Type | Fields | Values |
|------|--------|--------|
| `single` (default) | `user_answer`, `other_answer` | 1-N or 0 (Other) |
| `multi` | `user_answers` | List[int] |
| `yesno` | `user_answer`, `other_answer` | 1=Yes, 2=No, 3=Other |

### Answer Serialization (`Question.get_answer_dict()`)

```python
# single
{"index": 2, "option": "Paris"}
{"type": "Other", "value": "custom text"}

# multi
{"selected_indices": [1, 3], "selected_options": ["Python", "Rust"]}

# yesno
"Yes" | "No" | {"type": "Other", "value": "..."}
```

## YAML Format

```yaml
questions:
  - id: "q1"                    # optional
    question: "Question text"   # required
    type: single|multi|yesno    # optional, defaults to single
    options: ["A", "B", "C"]    # required for single/multi
    correct_answer: 2           # optional, 1-based index
```

After answering, `answer` and `metadata` fields are added automatically.

## Terminal Handling

- **Raw mode**: `termios` + `tty` via `raw_terminal()` context manager in `src/terminal.py`
- **Key sequences** (`src/navigation.py`): `\x1b[D` (left), `\x1b[C` (right), `\r`/`\n` (enter), `\x03` (Ctrl+C)

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Raw terminal mode | Single-char input, arrow keys, immediate feedback |
| Context manager | Always restores terminal state |
| Separate input handlers | Each question type has different patterns |
| `yaml.safe_load()` | Prevents code execution |

## Limitations

- **Platform**: Unix/macOS only. Windows needs `msvcrt`.
- **Display**: Full redraw per input (may flicker)

## Testing

```bash
uv run python tests/test_simple.py      # Quick validation
uv run python tests/test_mcq_tui.py     # Unit tests
uv run python tests/test_utilities.py   # Utility tests
```

## Dependencies

- `rich>=13.0.0`, `pyyaml>=6.0`, Python 3.8+


