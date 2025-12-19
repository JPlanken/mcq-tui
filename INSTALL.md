# Installation

## Quick Install

```bash
cd mcq-tui
uv pip install -e .
mcq --help
```

## Alternative: uv run (No PATH Setup)

```bash
cd mcq-tui
uv sync
uv run mcq questions.yaml
```

## Troubleshooting

### Command Not Found

1. Check installation: `uv pip list | grep mcq`
2. Check script: `ls ~/.local/bin/mcq`
3. Add to PATH if missing:

```bash
# zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc

# bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

4. Reinstall: `uv pip uninstall mcq && uv pip install -e .`

### Import Errors

```bash
# ModuleNotFoundError: No module named 'mcq_tui'
python3 -c "import mcq_tui; print('OK')"  # Test import
```

Verify `pyproject.toml`:
```toml
[tool.setuptools]
packages = ["src"]
py-modules = ["mcq_tui"]

[project.scripts]
mcq = "mcq_tui:main"
```
