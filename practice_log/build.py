"""`build`: check every skill's metadata against the open Agent Skills spec."""

import re
import sys

from practice_log.frontmatter import FrontmatterError, read_frontmatter

SPEC_FIELDS = ("name", "description", "license", "compatibility", "metadata", "allowed-tools")
# Literal ASCII classes: \w and \d would also accept non-ASCII letters and digits.
NAME_PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
NAME_MAX = 64
# claude.ai and the Claude API refuse skill names containing these words.
RESERVED_WORDS = ("anthropic", "claude")
# claude.ai's limit; the open spec allows 1024. Counted in characters, not bytes.
DESCRIPTION_MAX = 200
XML_TAG = re.compile(r"</?[A-Za-z][^<>]*>")


def run(root):
    skill_files = sorted((root / "skills").glob("*/SKILL.md"), key=lambda path: path.as_posix())
    if not skill_files:
        print("build: no skills found (expected skills/<name>/SKILL.md)", file=sys.stderr)
        return 1

    problems = []
    for skill_file in skill_files:
        label = skill_file.relative_to(root).as_posix()
        try:
            skill_problems = check_metadata(read_frontmatter(skill_file), skill_file.parent.name)
        except FrontmatterError as error:
            skill_problems = [str(error)]
        problems += [f"{label}: {problem}" for problem in skill_problems]

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f"build: metadata check failed ({plural(len(problems), 'problem')})", file=sys.stderr)
        return 1
    print(f"build: {plural(len(skill_files), 'skill')} checked, metadata ok")
    return 0


def plural(count, noun):
    return f"{count} {noun}{'' if count == 1 else 's'}"


def check_metadata(fields, folder):
    """Return the problems with one skill's frontmatter, in a stable order."""
    allowed = ", ".join(SPEC_FIELDS)
    problems = [
        f"field '{key}' is not one of the six open-spec fields ({allowed})"
        for key in sorted(fields)
        if key not in SPEC_FIELDS
    ]
    problems += check_name(fields.get("name"), folder)
    problems += check_description(fields.get("description"))
    return problems


def check_name(name, folder):
    if name is None:
        return ["missing required field 'name'"]
    if not isinstance(name, str) or len(name) > NAME_MAX or not NAME_PATTERN.fullmatch(name):
        return [
            f"name '{name}' must be 1-{NAME_MAX} lowercase ASCII letters, digits and single hyphens,"
            " with no hyphen at either end"
        ]
    problems = [f"name '{name}' contains the reserved word '{word}'" for word in RESERVED_WORDS if word in name]
    if name != folder:
        problems.append(f"name '{name}' does not match its folder '{folder}'")
    return problems


def check_description(description):
    if description is None:
        return ["missing required field 'description'"]
    if not isinstance(description, str):
        return ["description must be a single line of text"]
    if not description.strip():
        return ["description must not be empty"]
    problems = []
    if len(description) > DESCRIPTION_MAX:
        problems.append(f"description is {len(description)} characters, the limit is {DESCRIPTION_MAX} (claude.ai)")
    if XML_TAG.search(description):
        problems.append("description must not contain XML tags")
    return problems
