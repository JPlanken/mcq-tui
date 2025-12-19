# Testing

## Quick Start

```bash
python3 tests/test_simple.py       # Quick validation
python3 tests/test_mcq_tui.py      # Unit tests
python3 tests/test_utilities.py    # Utility tests
python3 tests/test_interactive.py  # Integration (requires pexpect)
```

## Smoke Testing (Manual UI)

For visual/formatting issues, see [SMOKE_TESTING.md](./SMOKE_TESTING.md).

```bash
# Run smoke tests with edge-case content
uv run python mcq_tui.py tests/fixtures/smoke_test.yaml
```

## Test Files

| File | Purpose | Dependencies |
|------|---------|--------------|
| `test_simple.py` | Quick validation | none |
| `test_mcq_tui.py` | Unit tests (Question, parsing, display) | none |
| `test_utilities.py` | Navigation, formatting utilities | none |
| `test_interactive.py` | TUI integration tests | pexpect |

## Manual Testing

```bash
python3 mcq_tui.py example_questions.yaml
```

Test scenarios:
1. Single-select: number keys → checkmark → Enter
2. Multi-select: multiple number keys → multiple checkmarks → Enter
3. Yes/No: 1/2/3 or y/n/o
4. Navigation: ← → j s q
5. Other option: 0 in single-select
6. Ctrl+C: clean exit with save prompt

## CI/CD

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Troubleshooting

- **pexpect not available**: `pip install pexpect` or skip `test_interactive.py`
- **Import errors**: `pip install rich pyyaml`
- **Interactive timeout**: Increase timeout in `test_interactive.py`
