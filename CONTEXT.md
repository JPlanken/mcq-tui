# Technical Context and Implementation Details

This document contains technical implementation details, design decisions, and internal architecture information for the MCQ TUI project.

## Architecture Overview

### Core Components

1. **Question Class** (`src/question.py`)
   - Represents a question with type-specific answer storage
   - Supports three types: `single`, `multi`, `yesno`
   - Tracks user answers differently per type:
     - Single: `user_answer` (int) + `other_answer` (str)
     - Multi: `user_answers` (List[int])
     - Yes/No: `user_answer` (int: 1/2/3) + `other_answer` (str)

2. **Display System** (`src/display.py`)
   - Uses Rich's `console.clear()` for full-screen redraws
   - Shows question type badge in header
   - Panel subtitle shows question type (multi-select, yes/no, single-select)
   - Visual feedback: bold green + checkmark for selected, dimmed for unselected

3. **Input Handlers** (`src/input_handlers.py`)
   - `get_multi_select_answer()`: Interactive toggle mode for multi-select
   - `get_single_select_answer()`: Interactive selection for single-select
   - `get_yesno_answer()`: Interactive selection for yes/no
   - All use raw terminal mode (`termios` + `tty`) for single-character input
   - Immediate visual feedback on number key press
   - Input handlers directly set question attributes (no need for re-processing)

### Input Handling

#### Raw Terminal Mode
- Uses `termios` and `tty` modules for raw character input
- Allows detection of arrow keys, Ctrl+C, and single character input
- Terminal settings are always restored in `finally` blocks
- Ctrl+C handling throughout ensures clean exit

#### Arrow Key Detection
- ESC sequence: `\x1b[` followed by `D` (left), `C` (right), `A` (up), `B` (down)
- Enter key: `\r` or `\n`
- Ctrl+C: `\x03`

#### Character Input Flow
1. Set terminal to raw mode
2. Read single character
3. Process character (arrow, digit, Enter, Ctrl+C, etc.)
4. Restore terminal settings
5. Update display or return result

### Question Type Implementation

#### Single-Select (`type: single`)
- Default type if not specified
- Answer stored as `user_answer: int` (1-N) or 0 for "Other"
- "Other" option requires text input via `Prompt.ask()`
- Visual: Selected option shows bold green + checkmark

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

### Display System

#### Visual Feedback Mechanism
- `display_question()` clears screen and redraws entire question
- Selected options: `[bold green]{num}[/bold green] [bold green]✓[/bold green]` + `[bold green]{text}[/bold green]`
- Unselected options: `[bold]{num}[/bold]` + `[dim]{text}[/dim]`
- Status header shows answer state with colored indicators

#### Panel Subtitle
- Uses Rich Panel's `subtitle` parameter
- Shows question type: `multi-select`, `yes/no`, `single-select`
- Appears at bottom of question panel

### Navigation System

#### Main Loop (`main()` function)
- Tracks `current_idx` (0-based) and `total`
- Displays question → Gets answer → Processes navigation/answer → Updates index
- Handles: quit, summary, jump, previous, next, answer input

#### Navigation Commands
- `q`: Quit (with confirmation)
- `s`: Show summary (with return option)
- `j`: Jump to question number
- `←`: Previous question
- `→` or Enter: Next question
- Ctrl+C: Immediate quit (no confirmation)

### Answer Processing

#### Answer Storage
- Answers stored directly in Question objects by input handlers
- Input handlers set question attributes when user selects answers
- Main loop only needs to check if answer exists and show result
- Summary reads from question objects to display answers

### Error Handling

#### KeyboardInterrupt (Ctrl+C)
- Caught at multiple levels:
  - Input functions restore terminal before re-raising
  - Main loop catches and exits cleanly
  - Always restores terminal settings

#### Terminal Restoration
- Every raw mode entry has corresponding restoration
- `finally` blocks ensure terminal is restored even on errors
- Multiple restoration points prevent terminal corruption

### YAML Parsing

#### Parser (`parse_yaml_questions()`)
- Uses `pyyaml.safe_load()` for parsing
- Handles missing `type` field (defaults to "single")
- Yes/No questions: options array optional (defaults to Yes/No)
- Validates: question text required, options required for single/multi

#### Format Validation
- Checks for `questions` array in YAML
- Validates each question has `question` field
- Validates options exist for single/multi types
- Graceful error messages for invalid formats

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

### Build System

#### Packaging (`pyproject.toml`)
- Build backend: `setuptools`
- Entry point: `mcq = mcq_tui:main`
- Single module package: `py-modules = ["mcq_tui"]`
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

#### Why Separate Input Functions?
- Each question type has different interaction patterns
- Multi-select: toggle mode (can select multiple)
- Single-select: selection mode (one at a time)
- Yes/No: simple selection (three options)
- Separation allows type-specific optimizations

#### Why Immediate Visual Feedback?
- Better UX: user sees selection immediately
- No need to press Enter to see feedback
- Consistent across all question types
- Reduces cognitive load

#### Why Checkmarks?
- Clear visual indicator of selection
- Works well with color coding (green = selected)
- Familiar pattern from GUI applications
- Distinguishes selected from unselected clearly

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
4. **Export Results**: Save answers to JSON/YAML file
5. **Question Validation**: Add validation rules (required questions, etc.)
6. **Keyboard Shortcuts**: More shortcuts for common actions
7. **Search**: Search questions by text
8. **Undo**: Undo last answer selection

### Code Organization

#### Function Structure
- `Question` class: Data model
- `parse_yaml_questions()`: File parsing
- `display_question()`: Display logic
- `get_*_answer()`: Input handlers (one per question type)
- `show_result()`: Answer confirmation display
- `show_summary()`: Final summary
- `main()`: Application entry point and main loop

#### Error Handling Strategy
- Graceful degradation: Show helpful error messages
- Terminal restoration: Always restore terminal state
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
- No file I/O during quiz (except initial load)

### Security Considerations

- Uses `yaml.safe_load()` (not `yaml.load()`) to prevent code execution
- No eval() or exec() usage
- File paths validated before reading
- User input sanitized before processing

