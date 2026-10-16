"""`mirror-plan`: print every Notion page the Mirror should hold, derived from the Practice Log.

It never talks to Notion: the practice-log-mirror skill writes the plan through the agent's connector,
or `mirror-push` writes it through Notion's API. The plan is a pure function of the workspace, so a re-run
with no Practice Log change prints the same pages. Each page links to its Problem's folder on GitHub,
from `mirror.repository` in the config. `mirror-record` keeps a hash of each page as last pushed in
mirror-state.json, so that `--changed` can leave out the pages a push wouldn't change.
The format is documented in skills/practice-log-mirror/references/mirror-pages.md; keep the two in step.
"""

import hashlib
import json
import re
import sys
from urllib.parse import quote

from practice_log.index import items, list_names, list_spellings, text
from practice_log.notes import read_key_takeaway
from practice_log.problems import read_problems
from practice_log.readme import plural
from practice_log.validate import DIFFICULTIES, OUTCOMES, is_date
from practice_log.workspace import CONFIG_FILE

DATABASE_TITLE = "Practice Log"
# The fixed schema of the database the Mirror creates. `Problem ID` is the key a push matches pages by.
# `Pending` is reserved for Attempts written straight to the Mirror from a chat app, which a push
# leaves alone until Import brings them home; every page in the plan has it unchecked.
PROPERTIES = [
    {"name": "Problem", "type": "title"},
    {"name": "Problem ID", "type": "text"},
    {"name": "Difficulty", "type": "select", "options": [difficulty.capitalize() for difficulty in DIFFICULTIES]},
    {"name": "Tags", "type": "multi_select"},
    {"name": "Lists", "type": "multi_select"},
    {"name": "Need Review", "type": "checkbox"},
    {"name": "Need Review Reason", "type": "text"},
    {"name": "Attempts", "type": "number"},
    {"name": "Last Attempt", "type": "date"},
    {"name": "Last Outcome", "type": "select", "options": list(OUTCOMES)},
    {"name": "Link", "type": "url"},
    {"name": "GitHub", "type": "url"},
    {"name": "Pending", "type": "checkbox"},
]
KEY = "Problem ID"
# Option colours. Difficulty and Last Outcome read like traffic lights; every Tags and Lists option gets a
# colour picked from its name, so it is the same on every push and machine.
FIXED_COLORS = {
    "Easy": "green", "Medium": "yellow", "Hard": "red",
    "solved-alone": "green", "solved-with-hints": "yellow", "saw-solution": "red",
}
PALETTE = ["gray", "brown", "orange", "yellow", "green", "blue", "purple", "pink", "red"]
# The default table view shows the columns of the learner's old Notion database, newest Attempt first;
# Problem ID, Need Review Reason, GitHub and Pending stay in the schema but out of that view.
VIEWS = [
    {
        "name": "All Problems",
        "type": "table",
        "show": ["Lists", "Difficulty", "Problem", "Tags", "Link", "Need Review", "Attempts", "Last Attempt", "Last Outcome"],
        "sort": [{"property": "Last Attempt", "direction": "descending"}],
    },
    {"name": "By Date", "type": "calendar", "calendar_by": "Last Attempt"},
]
# Notion refuses a text value over 2000 characters and a select option name holding a comma.
TEXT_MAX = 2000

PART = r"[A-Za-z0-9_.-]+"
GITHUB_REPOSITORY = [
    re.compile(rf"https://github\.com/({PART})/({PART}?)(?:\.git)?/?"),
    re.compile(rf"git@github\.com:({PART})/({PART}?)(?:\.git)?"),
    re.compile(rf"ssh://git@github\.com/({PART})/({PART}?)(?:\.git)?/?"),
]


STATE_FILE = "mirror-state.json"


class PlanError(ValueError):
    pass


def run(root, changed=False):
    try:
        plan = build_plan(root)
        if changed:
            plan = only_changed(plan, read_state(root))
    except PlanError as error:
        report(error)
        return 1
    if format == "browser":
        sys.stdout.write(browser(plan))
    else:
        sys.stdout.write(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    return 0


def report(error):
    for line in str(error).splitlines():
        print(line, file=sys.stderr)


def build_plan(root):
    config_file = root / CONFIG_FILE
    if not config_file.is_file():
        raise PlanError(
            f"mirror-plan: no {CONFIG_FILE} here, so this is not a Practice Workspace"
            " (create one with `practice-log init`)"
        )
    try:
        config = json.loads(config_file.read_text(encoding="utf-8-sig"))
    except ValueError as error:
        raise PlanError(f"mirror-plan: {CONFIG_FILE} is not valid JSON ({error})") from None
    mirror = config.get("mirror") if isinstance(config, dict) else None
    mirror = mirror if isinstance(mirror, dict) else {}
    repository = github_repository(mirror.get("repository"))

    notes = list(read_problems(root))
    errors = [problem.error for problem in notes if problem.error]
    if errors:
        raise PlanError(
            "\n".join(errors)
            + "\nmirror-plan: no plan printed; fix the notes (`practice-log validate` lists every error)"
        )
    spellings = list_spellings(notes)
    pages = []
    for problem in notes:
        folder = problem.folder
        problem_id = f"{folder.parent.name}:{folder.name}"
        takeaway = read_key_takeaway(problem.notes_file)
        lists = list_names(problem.fields, spellings)
        pages.append(page(repository, problem.rel, problem_id, problem.fields, lists, takeaway, problem.attempts))

    database_id = mirror.get("notion_database_id")
    return {
        "database": {
            "id": database_id if isinstance(database_id, str) and database_id else None,
            "title": DATABASE_TITLE,
            "description": (
                f"One-way Mirror of the Practice Log at {repository}, generated by LeetCode Tutor."
                " Edits made here are overwritten on the next push."
            ),
            "key": KEY,
            "properties": with_options(PROPERTIES, pages),
            "views": VIEWS,
        },
        "pages": pages,
    }


def with_options(properties, pages):
    """The fixed schema, with Tags and Lists carrying every value the pages use, sorted.

    Notion rejects a multi-select value that isn't already an option of the property.
    """
    result = []
    for prop in properties:
        if prop["type"] == "multi_select":
            used = {value for page in pages for value in page["properties"][prop["name"]]}
            prop = {**prop, "options": sorted(used)}
        if "options" in prop:
            prop = {**prop, "options": [{"name": name, "color": color(name)} for name in prop["options"]]}
        result.append(prop)
    return result


def github_repository(value):
    """The repository's https://github.com/<owner>/<repo> URL, from any form `git remote` prints."""
    if not isinstance(value, str) or not value.strip():
        raise PlanError(
            f"mirror-plan: {CONFIG_FILE} has no mirror.repository, so pages can't link to GitHub.\n"
            "Push the Practice Workspace to a GitHub repository, then set \"repository\" under \"mirror\""
            " to its URL, such as https://github.com/<owner>/<repo> (`git remote get-url origin` prints it)."
        )
    for pattern in GITHUB_REPOSITORY:
        match = pattern.fullmatch(value.strip())
        if match and match.group(2):
            return f"https://github.com/{match.group(1)}/{match.group(2)}"
    raise PlanError(
        f"mirror-plan: mirror.repository '{value}' is not a GitHub repository URL;"
        " use https://github.com/<owner>/<repo>"
    )


def page(repository, rel, problem_id, fields, lists, takeaway, attempts):
    # HEAD is the repository's default branch, so links survive a branch rename.
    folder_url = f"{repository}/tree/HEAD/{quote(rel)}"
    file_url = f"{repository}/blob/HEAD/{quote(rel)}/"
    difficulty = text(fields.get("difficulty")).lower()
    dated = [attempt for attempt in attempts if is_date(attempt.fields.get("date", ""))]
    # The latest date wins; on a tie, the later entry in the log.
    last = max(reversed(dated), key=lambda attempt: attempt.fields["date"], default=None)
    need_review = fields.get("need_review") == "true"
    outcome = last.fields.get("outcome") if last else None
    properties = {
        "Problem": clip(text(fields.get("title")) or problem_id),
        "Problem ID": clip(problem_id),
        "Difficulty": difficulty.capitalize() if difficulty in DIFFICULTIES else None,
        # Tags group case-insensitively, as the index shows them.
        "Tags": sorted({option(tag.lower()) for tag in items(fields.get("tags"))}),
        # Lists group case-insensitively too, each in its first spelling in the Practice Log.
        "Lists": list(dict.fromkeys(option(name) for name in lists)),
        "Need Review": need_review,
        "Need Review Reason": clip(text(fields.get("need_review_reason"))) if need_review else "",
        "Attempts": len(attempts),
        "Last Attempt": last.fields["date"] if last else None,
        "Last Outcome": outcome if outcome in OUTCOMES else None,
        "Link": text(fields.get("link")) or None,
        "GitHub": folder_url,
        "Pending": False,
    }
    return {"properties": properties, "body": body(folder_url, file_url, takeaway, attempts)}


def clip(value):
    return value if len(value) <= TEXT_MAX else value[: TEXT_MAX - 1] + "…"


def option(name):
    return name.replace(",", ";")


def body(folder_url, file_url, takeaway, attempts):
    parts = [
        f"> Generated from [this Problem's notes]({folder_url}) in the Practice Log."
        " Edits made here are overwritten on the next push: change the notes in the Practice Workspace instead.",
        "## Key Takeaway",
        takeaway or "None yet.",
        "## Attempts",
    ]
    if not attempts:
        parts.append("No Attempts yet.")
    for attempt in attempts:
        values = attempt.fields
        code = values.get("code", "")
        if code and "/" not in code and "\\" not in code:
            code = f"[{code}]({file_url}{quote(code)})"
        lines = [
            f"- {label}: {value}"
            for label, value in (
                ("Mode", values.get("mode", "")),
                ("Outcome", values.get("outcome", "")),
                ("Approach", values.get("approach", "")),
                ("Mistakes", values.get("mistakes", "")),
                ("Language", values.get("language", "")),
                ("Code", code),
                ("Origin", values.get("origin", "")),
            )
            if value
        ]
        parts.append(f"### {attempt.heading}\n\n" + "\n".join(lines) if lines else f"### {attempt.heading}")
    return "\n\n".join(parts) + "\n"


def color(name):
    """An option's colour: fixed for Difficulty and Last Outcome, otherwise stable per name."""
    if name in FIXED_COLORS:
        return FIXED_COLORS[name]
    digest = hashlib.sha256(name.lower().encode("utf-8")).digest()
    return PALETTE[digest[0] % len(PALETTE)]
# --- Only changed pages: mirror-state.json and mirror-record ---


def page_hash(page):
    """A short digest of everything a push writes for the page."""
    text = json.dumps(page, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def read_state(root, command="mirror-plan"):
    """The hashes recorded at the last push, or None when there are none."""
    path = root / STATE_FILE
    if not path.is_file():
        return None
    try:
        state = json.loads(path.read_text(encoding="utf-8-sig"))
    except ValueError as error:
        raise PlanError(f"{command}: {STATE_FILE} is not valid JSON ({error}); delete it to push every page") from None
    pages = state.get("pages") if isinstance(state, dict) else None
    if (
        state.get("version") != 1
        or not isinstance(pages, dict)
        or not all(isinstance(value, str) for value in pages.values())
    ):
        raise PlanError(f"{command}: {STATE_FILE} is not a Mirror state file; delete it to push every page")
    return state


def only_changed(plan, state):
    """The plan with only the pages whose content differs from the last push to the same database."""
    database_id = plan["database"]["id"]
    if state is None or database_id is None:
        since = "none"
    elif state.get("notion_database_id") != database_id:
        since = "other-database"
    else:
        since = "recorded"
    recorded = state["pages"] if since == "recorded" else {}
    pages, unchanged = [], []
    for page in plan["pages"]:
        problem_id = page["properties"][KEY]
        if recorded.get(problem_id) == page_hash(page):
            unchanged.append(problem_id)
        else:
            pages.append(page)
    in_plan = {page["properties"][KEY] for page in plan["pages"]}
    removed = sorted(problem_id for problem_id in recorded if problem_id not in in_plan)
    return {**plan, "pages": pages, "changes": {"state": since, "unchanged": unchanged, "removed": removed}}


def record(root, ids):
    """`mirror-record`: note pages as pushed, so the next `mirror-plan --changed` leaves them out.

    With no ids, every page in the plan. An id with no page in the plan is forgotten: its page was trashed.
    """
    try:
        plan = build_plan(root)
        state = read_state(root, "mirror-record")
    except PlanError as error:
        report(str(error).replace("mirror-plan:", "mirror-record:"))
        return 1
    database_id = plan["database"]["id"]
    if database_id is None:
        report(
            f"mirror-record: {CONFIG_FILE} has no mirror.notion_database_id, so there is no Mirror to record;"
            " store the database's id first"
        )
        return 1
    pages = dict(state["pages"]) if state and state.get("notion_database_id") == database_id else {}
    hashes = {page["properties"][KEY]: page_hash(page) for page in plan["pages"]}
    recorded = forgotten = 0
    for problem_id in ids or list(hashes):
        if problem_id in hashes:
            pages[problem_id] = hashes[problem_id]
            recorded += 1
        elif pages.pop(problem_id, None) is not None:
            forgotten += 1
    text = json.dumps(
        {"version": 1, "notion_database_id": database_id, "pages": dict(sorted(pages.items()))},
        ensure_ascii=False,
        indent=2,
    )
    (root / STATE_FILE).write_text(text + "\n", encoding="utf-8", newline="\n")
    summary = f"mirror-record: recorded {plural(recorded, 'page')} in {STATE_FILE}"
    if forgotten:
        summary += f", forgot {forgotten}"
    print(summary)
    return 0
