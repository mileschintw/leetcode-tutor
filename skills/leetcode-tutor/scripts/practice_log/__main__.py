"""practice-log: the deterministic CLI the LeetCode Tutor skills call. Standard library only.

Run it as `python -m practice_log` with the `scripts/` folder on PYTHONPATH, or as
`python <skill folder>/scripts/practice_log`, which needs no environment variable in any shell.
"""
import sys
from pathlib import Path

if not __package__:
    # Run as a folder path: Python put this folder on sys.path, but the package needs its parent.
    sys.path[0] = str(Path(__file__).resolve().parent.parent)

from practice_log.cli import main  # noqa: E402

sys.exit(main())
