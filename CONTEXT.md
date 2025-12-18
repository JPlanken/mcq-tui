# Technical Context and Implementation Details

This document contains technical implementation details, design decisions, and internal architecture information for the MCQ TUI project. For user-facing documentation, see [README.md](README.md).

## Architecture Overview

### Core Components

1. **Question Class** (`src/question.py`)
   - Represents a question with type-specific answer storage
   - Supports three types: `single`, `multi`, `yesno` (via `QuestionType` enum)
   - Tracks user answers differently per type:
     - Single: `user_answer` (int) + `other_answer` (str)
     - Multi: `user_answers` (List[int])
     - Yes/No: `user_answer` (int: 1/2/3) + `other_answer` (str)
   - Stores `question_id` (optional) for tracking questions across sessions
   - Provides `get_answer_dict()` method for serializable answer format

2. **Display System** (`src/display.py`)
   - Uses Rich's `console.clear()` for full-screen redraws
   - Shows question type badge in header
   - Panel subtitle shows question type (multi-select, yes/no, single-select)
   - Visual feedback: bold green + checkmark for selected, dimmed for unselected
   - Uses shared console instance from `src/console.py`

3. **Input Handlers** (`src/input_handlers.py`)
   - `get_multi_select_answer()`: Interactive toggle mode for multi-select
   - `get_single_select_answer()`: Interactive selection for single-select
   - `get_yesno_answer()`: Interactive selection for yes/no
   - All use `raw_terminal()` context manager from `src/terminal.py`
   - Immediate visual feedback on number key press
   - Input handlers directly set question attributes (no need for re-processing)

4. **Utility Modules**
   - `src/constants.py`: `QuestionType` and `NavCommand` enums
   - `src/console.py`: Shared `Console()` instance
   - `src/terminal.py`: `raw_terminal()` context manager for terminal management
   - `src/navigation.py`: Navigation utilities (hints formatting, command handling)
   - `src/answer_formatting.py`: Answer formatting utilities for consistent display
   - `src/export.py`: Answer export functionality (saves answers back to YAML)

### Input Handling

#### Raw Terminal Mode
- Uses `termios` and `tty` modules for raw character input
- Managed via `raw_terminal()` context manager (`src/terminal.py`)
- Allows detection of arrow keys, Ctrl+C, and single character input
- Terminal settings are always restored via context manager `finally` blocks
- Ctrl+C handling throughout ensures clean exit

#### Arrow Key Detection
- Handled by `handle_arrow_keys()` in `src/navigation.py`
- ESC sequence: `\x1b[` followed by `D` (left), `C` (right)
- Enter key: `\r` or `\n`
- Ctrl+C: `\x03`

#### Character Input Flow
1. Enter `raw_terminal()` context manager
2. Read single character
3. Process character via navigation utilities
4. Exit context manager (automatically restores terminal)
5. Update display or return result

### Question Type Implementation

#### Single-Select (`type: single`)
- Default type if not specified
- Answer stored as `user_answer: int` (1-N) or 0 for "Other"
- "Other" option requires text input via `Prompt.ask()`
- Visual: Selected option shows bold green + checkmark
- Requires Enter to confirm selection

#### Multi-Select (`type: multi`)
- Answer stored as `user_answers: List[int]`
- Uses interactive toggle mode (no text input prompt)
- Press number key to toggle selection on/off
- Visual: Multiple checkmarks possible, selection count shown
- Enter confirms selections

#### Yes/No (`type: yesno`)
- Answer stored as `user_answer: int` (1=Yes, 2=No, 3=Other)
- Options array optional (defaults to Yes/No)
- Supports both number keys (1/2/3) and letter keys (y/n/o)
- Visual: Selected option shows bold green + checkmark
- Requires Enter to confirm selection

### Display System

#### Visual Feedback Mechanism
- `display_question()` clears screen and redraws entire question
- Selected options: `[bold green]{num}[/bold green] [bold green]✓[/bold green]` + `[bold green]{text}[/bold green]`
- Unselected options: `[bold]{num}[/bold]` + `[dim]{text}[/dim]`
- Status header shows answer state with colored indicators
- Uses `get_answer_display_text()` and `get_answer_summary_text()` from `src/answer_formatting.py`

#### Panel Subtitle
- Uses Rich Panel's `subtitle` parameter
- Shows question type: `multi-select`, `yes/no`, `single-select`
- Appears at bottom of question panel

### Navigation System

#### Main Loop (`main()` function in `mcq_tui.py`)
- Tracks `current_idx` (0-based) and `total`
- Displays question → Gets answer → Processes navigation/answer → Updates index
- Handles: quit, summary, jump, previous, next, answer input
- Uses `NavCommand` enum constants from `src/constants.py`

#### Navigation Commands
- `q`: Quit (with confirmation)
- `s`: Show summary (with return option)
- `j`: Jump to question number
- `←`: Previous question
- `→` or Enter: Next question
- Ctrl+C: Immediate quit (no confirmation)
- Navigation hints formatted by `format_navigation_hints()` in `src/navigation.py`

### Answer Processing

#### Answer Storage
- Answers stored directly in Question objects by input handlers
- Input handlers set question attributes when user selects answers
- Main loop only needs to check if answer exists and show result
- Summary reads from question objects using `get_answer_summary_text()`
- Answers persist in memory throughout the quiz session

#### Answer Export (`src/export.py`)
- `export_results_to_yaml()`: Saves answers back to the original YAML file
- Matches questions by ID (or index if no ID) to preserve structure
- Adds `answer` field to each answered question in the YAML
- Adds `metadata` section with timestamp and statistics
- Automatically called when quiz completes or user exits
- Handles partial results (saves on Ctrl+C with confirmation)
- Preserves YAML structure while adding answer data

#### Answer Serialization
- `Question.get_answer_dict()`: Returns structured, JSON-serializable answer format
- Format varies by question type:
  - Single-select: `{index: int, option: str}` or `{type: "Other", value: str}`
  - Multi-select: `{selected_indices: List[int], selected_options: List[str]}`
  - Yes/No: `"Yes"`, `"No"`, or `{type: "Other", value: str}`
- Includes question ID, question text, type, and answer data
- Enables easy sharing of results with agents or other systems

### Error Handling

#### KeyboardInterrupt (Ctrl+C)
- Caught at multiple levels:
  - Input functions restore terminal before re-raising (via context manager)
  - Main loop catches and exits cleanly
  - Always restores terminal settings

#### Terminal Restoration
- `raw_terminal()` context manager ensures terminal is restored
- `finally` blocks in context manager prevent terminal corruption
- Multiple restoration points prevent terminal corruption

### YAML Parsing

#### Parser (`parse_yaml_questions()` in `src/parser.py`)
- Uses `pyyaml.safe_load()` for parsing
- Handles missing `type` field (defaults to `QuestionType.SINGLE`)
- Extracts `id` field from YAML (converts to string if numeric)
- Yes/No questions: options array optional (defaults to Yes/No)
- Validates: question text required, options required for single/multi
- Uses shared console instance for error messages

#### Format Validation
- Checks for `questions` array in YAML
- Validates each question has `question` field
- Validates options exist for single/multi types
- Graceful error messages for invalid formats
- Supports optional `id` field for question tracking

### Dependencies

#### Core Dependencies
- `rich`: Terminal UI library (console, panels, tables, prompts)
- `pyyaml`: YAML parsing

#### Standard Library
- `sys`: System operations, exit codes
- `termios`: Terminal control (Unix/macOS)
- `tty`: Terminal utilities
- `pathlib`: File path handling
- `typing`: Type hints
- `argparse`: CLI argument parsing
- `contextlib`: Context manager utilities

### Build System

#### Packaging (`pyproject.toml`)
- Build backend: `setuptools`
- Entry point: `mcq = mcq_tui:main`
- Package: `packages = ["src"]`
- Module: `py-modules = ["mcq_tui"]`
- Python requirement: `>=3.8`

#### Installation
- Uses `uv` for dependency management
- Editable install: `uv pip install -e .`
- Scripts installed to user's bin directory (`~/.local/bin`)

### Design Decisions

#### Why Raw Terminal Mode?
- Needed for single-character input without Enter
- Allows arrow key detection
- Enables immediate visual feedback
- Provides better UX than line-based input

#### Why Context Manager for Terminal?
- Ensures terminal is always restored, even on exceptions
- Reduces code duplication (was ~90 lines × 3, now ~20 lines reusable)
- Clear separation of concerns

#### Why Separate Input Functions?
- Each question type has different interaction patterns
- Multi-select: toggle mode (can select multiple)
- Single-select: selection mode (one at a time)
- Yes/No: simple selection (three options)
- Separation allows type-specific optimizations

#### Why Immediate Visual Feedback?
- Better UX: user sees selection immediately
- No need to press Enter to see feedback (but Enter still required to confirm)
- Consistent across all question types
- Reduces cognitive load

#### Why Checkmarks?
- Clear visual indicator of selection
- Works well with color coding (green = selected)
- Familiar pattern from GUI applications
- Distinguishes selected from unselected clearly

#### Why Utility Modules?
- Reduces code duplication (terminal management, navigation, formatting)
- Improves maintainability (changes in one place)
- Better testability (utilities can be tested independently)
- Type safety (constants prevent typos)

### Known Limitations

1. **Terminal Compatibility**
   - Uses Unix/macOS terminal APIs (`termios`, `tty`)
   - May not work on Windows without modifications
   - Arrow key sequences may vary by terminal

2. **Input Handling**
   - Raw mode disables normal terminal features
   - Terminal settings must be carefully restored
   - Complex escape sequences might not be handled

3. **Display Refresh**
   - Full screen clear on every update
   - May flicker on slow terminals
   - No partial updates (always full redraw)

### Future Improvements

1. **Windows Support**: Add Windows terminal support using `msvcrt` or `keyboard` library
2. **Partial Updates**: Only redraw changed portions for better performance
3. **Customizable Colors**: Allow theme customization
4. **Question Validation**: Add validation rules (required questions, etc.)
5. **Keyboard Shortcuts**: More shortcuts for common actions
6. **Search**: Search questions by text
7. **Undo**: Undo last answer selection
8. **Export Formats**: Support exporting to JSON, CSV, or other formats
9. **Answer History**: Track answer changes over time

### Code Organization

#### Module Structure
- `src/question.py`: Question data model with answer storage and serialization
- `src/parser.py`: YAML file parsing (reads questions and IDs)
- `src/display.py`: Display logic (questions, results, summary)
- `src/input_handlers.py`: Input handling (one function per question type)
- `src/export.py`: Answer export functionality (saves to YAML)
- `src/constants.py`: Constants and enums (`QuestionType`, `NavCommand`)
- `src/console.py`: Shared console instance
- `src/terminal.py`: Terminal management utilities
- `src/navigation.py`: Navigation utilities
- `src/answer_formatting.py`: Answer formatting utilities
- `mcq_tui.py`: Application entry point and main loop

#### Error Handling Strategy
- Graceful degradation: Show helpful error messages
- Terminal restoration: Always restore terminal state via context manager
- User-friendly errors: Clear messages, format examples
- KeyboardInterrupt: Clean exit at any time

### Testing Considerations

#### Manual Testing Required
- Terminal interaction requires manual testing
- Arrow key sequences vary by terminal
- Ctrl+C handling needs verification
- Visual feedback needs visual inspection

#### Test Scenarios
1. All question types (single, multi, yesno)
2. Navigation (arrows, Enter, commands)
3. Answer selection and visual feedback
4. Summary display
5. Error handling (invalid input, file not found)
6. Ctrl+C at various points
7. Edge cases (empty questions, no options, etc.)

### Performance Notes

- Full screen redraws on every input
- No caching of display state
- YAML parsing happens once at startup
- Question objects stored in memory
- File I/O only at startup (load) and completion/exit (save answers)
- Export operation is fast (single YAML write at end)

### Security Considerations

- Uses `yaml.safe_load()` (not `yaml.load()`) to prevent code execution
- No eval() or exec() usage
- File paths validated before reading
- User input sanitized before processing
