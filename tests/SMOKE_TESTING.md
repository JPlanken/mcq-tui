# MCQ-TUI Smoke Testing Plan

Manual testing plan to catch formatting issues, edge cases, and visual bugs.

## Quick Start

```bash
cd /Users/jonathanvanderplanken/Desktop/jpxp/mcq-tui
uv run python mcq_tui.py tests/fixtures/smoke_test.yaml
```

---

## Test Matrix

### Terminal Size Tests

| ID | Scenario | Terminal Size | Expected | Pass |
|----|----------|---------------|----------|------|
| T1 | Narrow terminal | 40×24 | Panels/tables wrap gracefully, no horizontal scroll | ☐ |
| T2 | Very narrow terminal | 30×24 | Content still readable, no crash | ☐ |
| T3 | Wide terminal | 200×24 | Content stays reasonable, no excessive whitespace | ☐ |
| T4 | Short terminal | 80×10 | Scrollable or visible prompt, no hidden input area | ☐ |
| T5 | Very short terminal | 80×5 | No crash, prompt still functional | ☐ |
| T6 | Minimum viable | 30×10 | Usable (degraded OK), no crash | ☐ |

**How to resize terminal:**
- macOS: Drag terminal window edges OR use `printf '\e[8;24;40t'` (rows;cols)
- iTerm: `Cmd+D` to split and shrink

---

### Content Edge Cases

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| C1 | Very long question text (200+ chars) | Text wraps inside panel, no overflow | ☐ |
| C2 | Single-word question | Panel renders correctly | ☐ |
| C3 | Question with special chars (!@#$%^&*) | Chars display correctly | ☐ |
| C4 | Question with unicode/emoji | Unicode renders (or gracefully degrades) | ☐ |
| C5 | Long option text (100+ chars) | Option wraps, number still visible | ☐ |
| C6 | Many options (10+) | All options visible (scroll OK) | ☐ |
| C7 | Single option | Works correctly | ☐ |
| C8 | Empty option text | Shows blank option row, no crash | ☐ |
| C9 | Long "Other" answer text | Input captured, displayed without overflow | ☐ |

---

### Question Type Tests

#### Single-Select (type: single)

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| S1 | Select option 1-9 | Checkmark appears, highlighted green | ☐ |
| S2 | Select option 0 (Other) | Prompt for text input appears | ☐ |
| S3 | Change selection before confirm | Previous selection cleared | ☐ |
| S4 | Enter without selection | Navigates to next or shows hint | ☐ |
| S5 | Re-visit answered question | Previous answer shown with checkmark | ☐ |

#### Multi-Select (type: multi)

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| M1 | Toggle single option | Checkmark appears/disappears | ☐ |
| M2 | Toggle multiple options | All selected show checkmarks | ☐ |
| M3 | Select all options | All show checkmarks | ☐ |
| M4 | Deselect all after selecting | Returns to "No selections" | ☐ |
| M5 | Enter with no selections | Shows "0 selected" or hint | ☐ |
| M6 | Counter updates correctly | "X selected" matches actual count | ☐ |

#### Yes/No (type: yesno)

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| Y1 | Press '1' or 'y' | Yes selected, checkmark on option 1 | ☐ |
| Y2 | Press '2' or 'n' | No selected, checkmark on option 2 | ☐ |
| Y3 | Press '3' or 'o' | Prompts for Other text | ☐ |
| Y4 | Toggle between Yes/No | Selection changes cleanly | ☐ |
| Y5 | Case insensitive (Y/N/O) | Works same as lowercase | ☐ |

---

### Navigation Tests

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| N1 | Press `←` on first question | No action (already at start) | ☐ |
| N2 | Press `←` on question 2+ | Returns to previous question | ☐ |
| N3 | Press `→` on middle question | Advances to next question | ☐ |
| N4 | Press `→` on last question | Shows summary or stays | ☐ |
| N5 | Press 'j' (jump) | Prompt for question number appears | ☐ |
| N6 | Jump to invalid number | Error message, returns to question | ☐ |
| N7 | Jump to valid number | Navigates correctly | ☐ |
| N8 | Press 's' (summary) | Summary view appears | ☐ |
| N9 | Press 'q' (quit) | Quit confirmation appears | ☐ |
| N10 | Ctrl+C at any point | Clean exit with save prompt | ☐ |
| N11 | Navigation hints update | ← hidden on Q1, → hidden on last Q | ☐ |

---

### Display Component Tests

#### Question Panel

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| P1 | Panel title shows "Question" | Title centered/visible | ☐ |
| P2 | Panel subtitle shows type | "[single-select]" etc. visible | ☐ |
| P3 | Panel border intact | Blue border, no broken chars | ☐ |
| P4 | Padding consistent | Text not touching borders | ☐ |

#### Options Table

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| O1 | Numbers aligned | 1, 2, 10 etc. in same column | ☐ |
| O2 | Checkmarks visible | Green ✓ appears after selection | ☐ |
| O3 | Dimmed unselected options | Unselected show dim styling | ☐ |
| O4 | Table spacing consistent | Rows evenly spaced | ☐ |

#### Summary View

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| SU1 | All columns visible | #, Type, Question, Answer | ☐ |
| SU2 | Long question truncated | Shows "..." after 37 chars | ☐ |
| SU3 | Long answer handling | Wraps or truncates gracefully | ☐ |
| SU4 | Statistics accurate | "Answered: X" matches reality | ☐ |
| SU5 | Table fits terminal width | No horizontal overflow | ☐ |

#### Answer Feedback Panel

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| F1 | Correct answer | Green border, ✓ symbol | ☐ |
| F2 | Incorrect answer | Red border, ✗ symbol | ☐ |
| F3 | Answer text visible | User answer + correct answer shown | ☐ |
| F4 | "Press Enter to continue" | Visible and functional | ☐ |

---

### Error Handling Tests

| ID | Scenario | Expected | Pass |
|----|----------|----------|------|
| E1 | File not found | Clear error message, exit cleanly | ☐ |
| E2 | Empty YAML file | "No questions found" message | ☐ |
| E3 | Malformed YAML | Error message (not crash) | ☐ |
| E4 | Missing required fields | Graceful handling or skip | ☐ |
| E5 | Invalid question type | Defaults to single or error | ☐ |

---

## Test Fixture

Create `tests/fixtures/smoke_test.yaml` with edge-case content:

```yaml
title: Smoke Test Questions
description: Edge cases for visual testing
questions:
  # Long question text
  - id: long-q
    question: "This is an extremely long question that is designed to test how the TUI handles text wrapping within the question panel. It should wrap gracefully without breaking the panel borders or causing horizontal scrolling. The question continues with more text to really stress-test the layout engine and ensure proper rendering."
    type: single
    options:
      - Short
      - "This option has a very long text that should test option wrapping behavior in the table display component"
      - Medium length option

  # Many options
  - id: many-opts
    question: "Select your favorite number (1-10)"
    type: multi
    options:
      - One
      - Two
      - Three
      - Four
      - Five
      - Six
      - Seven
      - Eight
      - Nine
      - Ten

  # Special characters
  - id: special-chars
    question: "Test special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
    type: yesno

  # Unicode/emoji
  - id: unicode
    question: "Do you like 🎉 emojis and ñ unicode chars? → ←"
    type: yesno

  # Single word
  - id: short
    question: "Continue?"
    type: yesno

  # Single option
  - id: single-opt
    question: "Only one choice available:"
    type: single
    options:
      - "The only option"

  # Yes/No with Other
  - id: yesno-other
    question: "Is this test comprehensive?"
    type: yesno

  # Correct answer feedback test
  - id: feedback
    question: "What is 2+2?"
    type: single
    options:
      - "3"
      - "4"
      - "5"
    correct_answer: 2
```

---

## Quick Resize Commands (macOS)

```bash
# Set terminal to specific size (rows x cols)
printf '\e[8;24;40t'   # 40 cols x 24 rows (narrow)
printf '\e[8;24;80t'   # 80 cols x 24 rows (standard)
printf '\e[8;24;200t'  # 200 cols x 24 rows (wide)
printf '\e[8;10;80t'   # 80 cols x 10 rows (short)
printf '\e[8;5;30t'    # 30 cols x 5 rows (minimum)
```

---

## Regression Checklist

After fixes, verify:

- [ ] All terminal sizes from T1-T6 still work
- [ ] No new wrapping issues introduced
- [ ] Performance acceptable (no visible lag)
- [ ] Colors render correctly
- [ ] Terminal state restored after exit

---

## Issue Log

| Date | Issue Found | Test ID | Severity | Fixed |
|------|-------------|---------|----------|-------|
| | | | | |

---

## Notes

- Run tests in a fresh terminal (not tmux/screen initially) to avoid interaction issues
- Test both light and dark terminal themes if possible
- Check with different fonts (monospace required)
