"""A small reader for the YAML frontmatter at the top of a Markdown file.

It understands only what skill metadata needs: top-level `key: value` scalars (plain or quoted,
with optional ` # comment`) and one level of indented `key: value` pairs under a key with no value
(`metadata:`). A key with no value and nothing indented under it is an empty string.
"""

import re

COMMENT = re.compile(r"\s+#.*$")


class FrontmatterError(ValueError):
    pass


def read_text(path):
    """The file's text; a file that isn't UTF-8 raises FrontmatterError rather than a traceback."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as error:
        raise FrontmatterError(f"not valid UTF-8 (byte {error.start}); save the file as UTF-8") from None


def read_frontmatter(path):
    """Return the frontmatter of `path` as a dict of strings and string-to-string dicts."""
    lines = read_text(path).splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("missing frontmatter (the file must start with a '---' line)")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise FrontmatterError("unterminated frontmatter (no closing '---' line)") from None

    fields = {}
    current_map = None
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line[0] in " \t"
        key, sep, value = line.strip().partition(":")
        key, value = key.strip(), value.strip()
        if not sep or not key:
            raise FrontmatterError(f"frontmatter line {line_number}: expected 'key: value'")
        target = fields
        if indented:
            if current_map is None:
                raise FrontmatterError(f"frontmatter line {line_number}: unexpected indentation")
            target = current_map
        if key in target:
            raise FrontmatterError(f"frontmatter line {line_number}: duplicate field '{key}'")
        value = _scalar(value, line_number)
        if indented:
            target[key] = value
        elif value:
            target[key] = value
            current_map = None
        else:
            current_map = target[key] = {}
    # A key with no value and no indented pairs under it is an empty scalar, not an empty map.
    return {key: "" if value == {} else value for key, value in fields.items()}


def _scalar(value, line_number):
    if value and value[0] in "\"'":
        closing = value.find(value[0], 1)
        if closing == -1 or COMMENT.sub("", value[closing + 1 :]).strip():
            raise FrontmatterError(f"frontmatter line {line_number}: unsupported or unterminated value")
        return value[1:closing]
    value = COMMENT.sub("", value)
    if value and value[0] in "|>":
        raise FrontmatterError(
            f"frontmatter line {line_number}: block scalars are not supported, keep the value on one line"
        )
    if value and value[0] in "[{":
        raise FrontmatterError(f"frontmatter line {line_number}: unsupported or unterminated value")
    return value
