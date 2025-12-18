"""
Terminal management utilities for raw mode input handling
"""

import sys
import termios
import tty
from contextlib import contextmanager
from typing import Generator


@contextmanager
def raw_terminal() -> Generator[None, None, None]:
    """
    Context manager for raw terminal mode.
    Ensures terminal settings are always restored, even on exceptions.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        yield
    finally:
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            pass
