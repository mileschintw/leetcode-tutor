"""A reader for a Problem's notes.md: flat YAML frontmatter and the Attempt log.

The frontmatter reader understands what Obsidian writes for flat properties: `key: value` scalars
(plain or quoted, with optional ` # comment`), flow lists (`[a, b]`) and block lists (`- item` lines
under a key with no value). The Attempt log is every `### ` heading under `## Attempts`, each followed
by `- key: value` lines.
"""

import re

COMMENT = re.compile(r"\s+#.*$")
LIST_ITEM = re.compile(r"^\s*-\s+(.*)$")
ATTEMPT_FIELD = re.compile(r"^-\s+([A-Za-z_]+)\s*:(.*)$")


class NotesError(ValueError):
    pass


class Attempt:
    def __init__(self, heading, line_number):
        self.heading = heading
        self.line_number = line_number
        self.fields = {}
        self.problems = []


def read_notes(path):
    """Return (frontmatter fields, list of Attempts) for one notes file."""
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except UnicodeDecodeError as error:
        raise NotesError(f"not valid UTF-8 (byte {error.start}); save the file as UTF-8") from None
    if not lines or lines[0].strip() != "---":
        raise NotesError("missing frontmatter (the file must start with a '---' line)")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise NotesError("unterminated frontmatter (no closing '---' line)") from None
    return _frontmatter(lines[1:end]), _attempts(lines, end + 1)


def _frontmatter(lines):
    fields = {}
    list_key = None
    empty = set()  # keys with no value and, so far, no `- item` lines
    for line_number, line in enumerate(lines, start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = LIST_ITEM.match(line)
        if item:
            if list_key is None:
                raise NotesError(f"frontmatter line {line_number}: list item without a key")
            fields[list_key].append(_scalar(item.group(1).strip(), line_number))
            empty.discard(list_key)
            continue
        if line[0] in " \t":
            raise NotesError(f"frontmatter line {line_number}: unexpected indentation")
        key, sep, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if not sep or not key:
            raise NotesError(f"frontmatter line {line_number}: expected 'key: value'")
        if key in fields:
            raise NotesError(f"frontmatter line {line_number}: duplicate field '{key}'")
        value = COMMENT.sub("", value) if value[:1] not in "\"'" else value
        if not value:
            # Empty for now; becomes a list if `- item` lines follow.
            fields[key] = []
            list_key = key
            empty.add(key)
            continue
        list_key = None
        fields[key] = _flow_list(value, line_number) if value.startswith("[") else _scalar(value, line_number)
    # A key with no value and no items under it is an empty scalar.
    return {key: "" if key in empty else value for key, value in fields.items()}


def _scalar(value, line_number):
    if value and value[0] in "\"'":
        closing = value.find(value[0], 1)
        if closing == -1 or COMMENT.sub("", value[closing + 1 :]).strip():
            raise NotesError(f"frontmatter line {line_number}: unterminated quoted value")
        return value[1:closing]
    value = COMMENT.sub("", value)
    if value[:1] in ("|", ">", "{"):
        raise NotesError(f"frontmatter line {line_number}: keep each value on one line as plain text or a list")
    return value


def _flow_list(value, line_number):
    if not value.endswith("]"):
        raise NotesError(f"frontmatter line {line_number}: unterminated list")
    inner = value[1:-1].strip()
    if not inner:
        return []
    items, current, quote = [], "", None
    for char in inner:
        if quote:
            current += char
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
            current += char
        elif char == ",":
            items.append(current.strip())
            current = ""
        else:
            current += char
    items.append(current.strip())
    return [_scalar(item, line_number) for item in items]


def _attempts(lines, start):
    attempts = []
    in_log = False
    for line_number, line in enumerate(lines[start:], start=start + 1):
        if line.startswith("## "):
            in_log = line[3:].strip().lower() == "attempts"
            continue
        if not in_log:
            continue
        if line.startswith("### "):
            attempts.append(Attempt(line[4:].strip(), line_number))
            continue
        field = ATTEMPT_FIELD.match(line.strip())
        if field and attempts:
            key, value = field.group(1), field.group(2).strip()
            attempt = attempts[-1]
            if key in attempt.fields:
                attempt.problems.append(f"line {line_number}: duplicate field '{key}'")
            else:
                attempt.fields[key] = value
    return attempts


def read_key_takeaway(path):
    """The text under `## Key Takeaway`, stripped; empty when the section is missing or blank."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    section, inside = [], False
    for line in lines:
        if line.startswith("## "):
            inside = line[3:].strip().lower() == "key takeaway"
            continue
        if inside:
            section.append(line)
    return "\n".join(section).strip()


def read_key_takeaway_line(path):
    """The text under a notes file's `## Key Takeaway` heading, as one line ("" when there is none)."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    body, in_section = [], False
    for line in lines:
        if line.startswith("## "):
            in_section = line[3:].strip().lower() == "key takeaway"
            continue
        if in_section and line.strip():
            body.append(line.strip())
    return " ".join(body)
