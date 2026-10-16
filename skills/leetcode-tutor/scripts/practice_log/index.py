"""`index`: regenerate the Practice Workspace's README.md from the Practice Log.

It reads only what the notes hold: the Attempt count and last Attempt date come from each Problem's
Attempt log. It checks nothing `validate` checks, but writes nothing when a notes file is unreadable.
"""

import sys

from practice_log import readme
from practice_log.readme import README_FILE
from practice_log.problems import read_problems
from practice_log.validate import is_date
from practice_log.workspace import CONFIG_FILE


def run(root):
    if not (root / CONFIG_FILE).is_file():
        print(
            f"index: no {CONFIG_FILE} here, so this is not a Practice Workspace"
            " (create one with `practice-log init`)",
            file=sys.stderr,
        )
        return 1

    notes = list(read_problems(root))
    errors = [n.error for n in notes if n.error]
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"index: {README_FILE} not written; fix the notes (`practice-log validate` lists every error)", file=sys.stderr)
        return 1

    spellings = list_spellings(notes)
    problems = [to_problem(n.rel, n.fields, n.attempts, spellings) for n in notes]
    (root / README_FILE).write_text(readme.render(problems), encoding="utf-8", newline="\n")
    attempts = sum(p.attempts for p in problems)
    print(f"index: wrote {README_FILE} ({readme.plural(len(problems), 'Problem')}, {readme.plural(attempts, 'Attempt')})")
    return 0


def to_problem(rel, fields, attempts, spellings):
    problem_id = text(fields.get("id"))
    dates = [attempt.fields.get("date", "") for attempt in attempts]
    return readme.Problem(
        folder=rel,
        problem_id=problem_id,
        title=text(fields.get("title")) or problem_id or rel,
        difficulty=text(fields.get("difficulty")),
        # Tags group case-insensitively and show in lowercase, as the schema writes them.
        tags=sorted({tag.lower() for tag in items(fields.get("tags"))}),
        lists=list_names(fields, spellings),
        need_review=fields.get("need_review") == "true",
        reason=text(fields.get("need_review_reason")),
        # An Attempt with a malformed date still counts, but never sets the last date.
        dates=[date if is_date(date) else "" for date in dates],
    )


def text(value):
    if value is None:
        return ""
    return value if isinstance(value, str) else ", ".join(value)


def items(value):
    """A list field's names; a single value counts as one name, an empty one as none."""
    if isinstance(value, list):
        return [item for item in value if item]
    return [value] if value else []


def list_spellings(notes):
    """Each Problem List name, case-folded, mapped to its first spelling in folder order.

    Problem Lists group regardless of case, as `review-sheet --list` matches them, so `Grind 75` and
    `grind 75` are one list, shown as it was first written.
    """
    spellings = {}
    for problem in notes:
        for name in items(problem.fields.get("lists")):
            spellings.setdefault(name.casefold(), name)
    return spellings


def list_names(fields, spellings):
    """A Problem's Problem Lists in the notes' order, each in its first spelling, once."""
    return list(dict.fromkeys(spellings[name.casefold()] for name in items(fields.get("lists"))))
