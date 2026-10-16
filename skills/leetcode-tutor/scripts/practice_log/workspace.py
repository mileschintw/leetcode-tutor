"""`init`: create a Practice Workspace in a new or empty folder."""

import sys

from practice_log import readme

CONFIG_FILE = "practice-log.json"

CONFIG = """\
{
  "version": 1,
  "mirror": {
    "notion_database_id": null
  }
}
"""

README = readme.render([])

GITIGNORE = """\
# Editors and operating systems
.DS_Store
Thumbs.db
.vscode/
.idea/

# Obsidian: keep shared settings, skip per-device layout
.obsidian/workspace*.json
.trash/

# Code from local runs
__pycache__/
*.pyc
.venv/
node_modules/
*.class
*.o
*.out
"""

GITATTRIBUTES = """\
* text=auto eol=lf
"""

FILES = {
    CONFIG_FILE: CONFIG,
    readme.README_FILE: README,
    ".gitignore": GITIGNORE,
    ".gitattributes": GITATTRIBUTES,
    # Git keeps no empty folders.
    "problems/.gitkeep": "",
    "review-sheets/.gitkeep": "",
}


def run(target):
    label = target.as_posix()
    if target.exists() and not target.is_dir():
        print(f"init: {label} is a file, not a folder", file=sys.stderr)
        return 1
    if (target / CONFIG_FILE).exists():
        print(f"init: {label} is already a Practice Workspace ({CONFIG_FILE} exists)", file=sys.stderr)
        return 1
    # A folder that only holds a fresh `git init` still counts as empty.
    if target.is_dir() and any(entry.name != ".git" for entry in target.iterdir()):
        print(f"init: {label} is not empty; choose a new or empty folder", file=sys.stderr)
        return 1

    for name, text in FILES.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    print(f"init: created a Practice Workspace in {label}")
    return 0
