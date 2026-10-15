"""A small reader for the YAML frontmatter at the top of a Markdown file.

It understands only what skill metadata needs: top-level `key: value` scalars (plain or quoted)
and one level of indented `key: value` pairs under a key with no value (`metadata:`).
"""


class FrontmatterError(ValueError):
    pass


def read_frontmatter(path):
    """Return the frontmatter of `path` as a dict of strings and string-to-string dicts."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("missing frontmatter (the file must start with a '---' line)")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise FrontmatterError("unterminated frontmatter (no closing '---' line)") from None

    fields = {}
    current_map = None
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line[0] in " \t"
        key, sep, value = line.strip().partition(":")
        key, value = key.strip(), value.strip()
        if not sep or not key:
            raise FrontmatterError(f"frontmatter line {number}: expected 'key: value'")
        if indented:
            if current_map is None:
                raise FrontmatterError(f"frontmatter line {number}: unexpected indentation")
            current_map[key] = _scalar(value, number)
            continue
        if key in fields:
            raise FrontmatterError(f"frontmatter line {number}: duplicate field '{key}'")
        if value:
            fields[key] = _scalar(value, number)
            current_map = None
        else:
            current_map = fields[key] = {}
    return fields


def _scalar(value, number):
    if value[:1] in "|>":
        raise FrontmatterError(f"frontmatter line {number}: block scalars are not supported, keep the value on one line")
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value[:1] in "\"'[{":
        raise FrontmatterError(f"frontmatter line {number}: unsupported or unterminated value")
    return value
