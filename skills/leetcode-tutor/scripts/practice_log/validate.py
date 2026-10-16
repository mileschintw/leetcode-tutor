"""`validate`: check a Practice Workspace against the Practice Log schema (references/practice-log.md)."""

import datetime
import json
import re
import sys

from practice_log.problems import read_problems
from practice_log.workspace import CONFIG_FILE

PART = r"[a-z0-9]+(?:-[a-z0-9]+)*"
PROBLEM_ID = re.compile(rf"({PART}):({PART})")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

DIFFICULTIES = ("easy", "medium", "hard")
MODES = ("session", "recap")
OUTCOMES = ("solved-alone", "solved-with-hints", "saw-solution")
BOOLEANS = ("true", "false")
LIST_FIELDS = ("tags", "lists")
ATTEMPT_REQUIRED = ("date", "mode", "outcome", "approach", "language", "code")


def run(root):
    config = root / CONFIG_FILE
    if not config.is_file():
        print(
            f"validate: no {CONFIG_FILE} here, so this is not a Practice Workspace"
            " (create one with `practice-log init`)",
            file=sys.stderr,
        )
        return 1

    problems = check_config(config)
    seen = {}
    attempt_count = 0
    problem_count = 0
    for problem in read_problems(root):
        if problem.error:
            problems.append(problem.error)
            continue
        problem_count += 1
        folder, label, fields, attempts = problem.folder, problem.notes_label, problem.fields, problem.attempts
        attempt_count += len(attempts)
        file_problems = check_problem(fields, folder)
        for number, attempt in enumerate(attempts, start=1):
            prefix = f"attempt {number} ({attempt.heading})"
            file_problems += [f"{prefix}: {problem}" for problem in attempt.problems + check_attempt(attempt, folder)]
        problem_id = fields.get("id")
        if isinstance(problem_id, str) and problem_id:
            if problem_id in seen:
                file_problems.append(f"duplicate id '{problem_id}' (also in {seen[problem_id]})")
            else:
                seen[problem_id] = label
        problems += [f"{label}: {problem}" for problem in file_problems]
    problems += misplaced_notes(root)

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f"validate: failed ({plural(len(problems), 'error')})", file=sys.stderr)
        return 1
    print(f"validate: {plural(problem_count, 'Problem')}, {plural(attempt_count, 'Attempt')}, ok")
    return 0


def plural(count, noun):
    return f"{count} {noun}{'' if count == 1 else 's'}"


def misplaced_notes(root):
    """notes.md files above the problems/<source>/<slug>/ level, which the Problem walk skips.

    One deeper down is the learner's own file in a Problem folder, and stays as it is.
    """
    problems_dir = root / "problems"
    return [
        f"{notes.relative_to(root).as_posix()}: notes.md must be in a problems/<source>/<slug>/ folder"
        for notes in sorted(problems_dir.rglob("notes.md"), key=lambda path: path.as_posix())
        if len(notes.relative_to(problems_dir).parts) < 3
    ]


def check_config(config):
    try:
        data = json.loads(config.read_text(encoding="utf-8-sig"))
    except ValueError as error:
        return [f"{CONFIG_FILE}: not valid JSON ({error})"]
    version = data.get("version") if isinstance(data, dict) else None
    # bool is an int subclass and 1.0 == 1, so `true` and `1.0` would otherwise pass.
    if type(version) is not int or version != 1:
        return [f"{CONFIG_FILE}: expected an object with \"version\": 1"]
    return []


def check_problem(fields, folder):
    problems = [f"missing required field '{key}'" for key in ("id", "title", "need_review") if not fields.get(key)]
    for key, value in fields.items():
        if key not in LIST_FIELDS and isinstance(value, list):
            problems.append(f"{key} must be a single value, not a list")

    problem_id = fields.get("id")
    if isinstance(problem_id, str) and problem_id:
        match = PROBLEM_ID.fullmatch(problem_id)
        if not match:
            problems.append(
                f"id '{problem_id}' must be '<source>:<slug>', each part lowercase ASCII letters,"
                " digits and single hyphens"
            )
        elif match.groups() != (folder.parent.name, folder.name):
            problems.append(f"id '{problem_id}' does not match its folder (expected '{folder.parent.name}:{folder.name}')")

    problems += check_enum("difficulty", fields.get("difficulty"), DIFFICULTIES)
    need_review = fields.get("need_review")
    problems += check_enum("need_review", need_review, BOOLEANS)
    if need_review == "true" and not fields.get("need_review_reason"):
        problems.append("missing required field 'need_review_reason' (need_review is true)")
    for key in LIST_FIELDS:
        if key in fields and not isinstance(fields[key], list) and fields[key] != "":
            problems.append(f"{key} must be a list, such as [a, b]")
    return problems


def check_attempt(attempt, folder):
    fields = attempt.fields
    problems = [f"missing required field '{key}'" for key in ATTEMPT_REQUIRED if not fields.get(key)]
    date = fields.get("date")
    if date and not is_date(date):
        problems.append(f"date '{date}' must be a real date written YYYY-MM-DD")
    problems += check_enum("mode", fields.get("mode"), MODES)
    problems += check_enum("outcome", fields.get("outcome"), OUTCOMES)
    code = fields.get("code")
    if code and ("/" in code or "\\" in code or code in (".", "..")):
        problems.append(f"code '{code}' must be a file name in the Problem's folder, not a path")
    # Compare names exactly: is_file() ignores case on Windows and macOS but not on Linux.
    elif code and code not in {path.name for path in folder.iterdir() if path.is_file()}:
        problems.append(f"code file '{code}' not found in {folder.name}/")
    return problems


def check_enum(key, value, allowed):
    # A list value is reported once, as "must be a single value".
    if not isinstance(value, str) or not value or value in allowed:
        return []
    return [f"{key} '{value}' must be one of {', '.join(allowed)}"]


def is_date(text):
    if not DATE.fullmatch(text):
        return False
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        return False
    return True
