"""`build`: check the skills against the platforms' constraints, then generate every release artefact.

Committed artefacts (copy-paste prompts, plugin manifests) are written in place; `--check` instead
verifies they are up to date and writes nothing. Upload zips go to the gitignored dist/.
"""

import json
import re
import shutil
import sys

from practice_log import package
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


def run(root, check=False):
    skill_files = sorted((root / "skills").glob("*/SKILL.md"), key=lambda path: path.as_posix())
    if not skill_files:
        print("build: no skills found (expected skills/<name>/SKILL.md)", file=sys.stderr)
        return 1

    problems = []
    names = {skill_file.parent.name for skill_file in skill_files}
    requires = {}  # skill name -> the skill it needs installed alongside it
    for skill_file in skill_files:
        label = skill_file.relative_to(root).as_posix()
        folder = skill_file.parent.name
        try:
            fields = read_frontmatter(skill_file)
        except FrontmatterError as error:
            problems.append(f"{label}: {error}")
            continue
        skill_problems = check_metadata(fields, folder)
        required = required_skill(fields)
        if required is not None:
            requires[folder] = required
            skill_problems += check_required(required, folder, names)
        problems += [f"{label}: {problem}" for problem in skill_problems]
    problems += check_layout(root)
    problems += [f"{package.CLAUDE_PLUGIN}: {problem}" for problem in check_claude_plugin(root)]

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f"build: metadata check failed ({plural(len(problems), 'problem')})", file=sys.stderr)
        return 1
    print(f"build: {plural(len(skill_files), 'skill')} checked, metadata ok")

    # A skill that needs another installed alongside it can't work as a pasted prompt or an upload zip.
    skill_dirs = [skill_file.parent for skill_file in skill_files if skill_file.parent.name not in requires]
    for name in sorted(requires):
        print(f"build: {name} requires {requires[name]}, so it gets no prompt or upload zips")
    committed = package.committed_artefacts(root, skill_dirs)
    obsolete = [f"{package.PROMPTS_DIR}/{name}.md" for name in sorted(requires)]
    obsolete = [rel for rel in obsolete if (root / rel).exists()]
    if check:
        return check_committed(root, committed, obsolete)

    dist = root / package.DIST_DIR
    if dist.exists():
        shutil.rmtree(dist)
    artefacts = {**committed, **package.dist_artefacts(skill_dirs)}
    for rel in sorted(artefacts):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(artefacts[rel])
        print(f"build: wrote {rel}")
    for rel in obsolete:
        (root / rel).unlink()
        print(f"build: removed {rel}")
    return 0


def check_committed(root, committed, obsolete):
    stale = [f"{rel}: no longer generated" for rel in obsolete]
    for rel in sorted(committed):
        path = root / rel
        if not path.exists():
            stale.append(f"{rel}: missing")
        # A Windows checkout may hold CRLF copies of what build writes with LF.
        elif path.read_bytes().replace(b"\r\n", b"\n") != committed[rel]:
            stale.append(f"{rel}: out of date")
    if stale:
        for problem in stale:
            print(problem, file=sys.stderr)
        print(f"build: generated files are stale, run `{package.BUILD_COMMAND}` and commit", file=sys.stderr)
        return 1
    print(f"build: {plural(len(committed), 'generated file')} up to date")
    return 0


def check_layout(root):
    if (root / "bin").is_dir():
        return ["bin/: a top-level bin directory makes claude.ai refuse the whole plugin"]
    return []


def check_claude_plugin(root):
    """Problems with the manifest the other tools' manifests are generated from (it is optional)."""
    path = root / package.CLAUDE_PLUGIN
    if not path.exists():
        return []
    try:
        plugin = json.loads(path.read_text(encoding="utf-8-sig"))
    except ValueError as error:
        return [f"not valid JSON ({error})"]
    if not isinstance(plugin, dict):
        return ["must be a JSON object"]
    problems = []
    name = plugin.get("name")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        problems.append("'name' must be lowercase ASCII letters, digits and single hyphens")
    description = plugin.get("description")
    if not isinstance(description, str) or not description.strip():
        problems.append("'description' must be non-empty text")
    author = plugin.get("author")
    if author is not None and not (
        isinstance(author, str) or (isinstance(author, dict) and isinstance(author.get("name"), str))
    ):
        problems.append("'author' must be a name or an object with a 'name'")
    if "repository" in plugin and not isinstance(plugin["repository"], str):
        problems.append("'repository' must be a URL string")
    return problems


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


def required_skill(fields):
    """The skill named by `metadata: requires:`, which must be installed alongside this one."""
    metadata = fields.get("metadata")
    return metadata.get("requires") if isinstance(metadata, dict) else None


def check_required(required, folder, names):
    if required == folder:
        return ["metadata 'requires' names the skill itself"]
    if required not in names:
        return [f"metadata 'requires' names '{required}', which is not a skill in skills/"]
    return []


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
