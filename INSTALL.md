# Installation Guide

## Install as Command-Line Tool

### Quick Install

```bash
cd mcq-tui
uv pip install -e .
```

That's it! The `mcq` command should now be available.

**If `mcq` command not found:**

Most systems already have `~/.local/bin` in PATH. If yours doesn't, add this to `~/.zshrc` (or `~/.bashrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.zshrc
```

**Usage:**
```bash
mcq questions.yaml
mcq --help
```

## Development Installation

For development with isolated environment:

```bash
cd mcq-tui
uv sync
uv run mcq questions.yaml
```

## Verify Installation

```bash
which mcq
mcq --help
mcq example_questions.yaml
```

## Troubleshooting

### Command Not Found After Install

**Step 1: Verify the script was created**
```bash
ls -la ~/.local/bin/mcq
```

If the file doesn't exist, the installation didn't create the entry point script.

**Step 2: Check if package is installed**
```bash
uv pip list | grep mcq
# or
pip list | grep mcq
```

**Step 3: Reinstall**
```bash
cd mcq-tui
uv pip uninstall mcq
uv pip install -e .
```

**Step 4: Verify PATH**
```bash
echo $PATH | tr ':' '\n' | grep local
```

If `~/.local/bin` is not in the output, add it:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Step 5: Test the installation**
```bash
which mcq          # Should show: ~/.local/bin/mcq
mcq --help         # Should show help text
```

### Alternative: Use `uv run` (No PATH Setup Needed)

If PATH setup is problematic, use `uv run` instead:

```bash
cd mcq-tui
uv sync
uv run mcq questions.yaml
```

This works without any PATH configuration.

### Module Import Errors

If you see `ModuleNotFoundError: No module named 'mcq_tui'`:

1. Verify `mcq_tui.py` exists in the project root
2. Test import: `python3 -c "import mcq_tui; print('OK')"`
3. Check `pyproject.toml` has: `[tool.setuptools] py-modules = ["mcq_tui"]`

### Entry Point Errors

If you see `AttributeError: module 'mcq_tui' has no attribute 'main'`:

1. Verify `main()` function exists in `mcq_tui.py`
2. Check entry point matches: `[project.scripts] mcq = "mcq_tui:main"`
