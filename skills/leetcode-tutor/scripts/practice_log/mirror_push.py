"""`mirror-push`: write the Mirror plan to Notion through Notion's public REST API.

A deterministic way to push when no Notion connector is available. It reads the integration token from
the NOTION_TOKEN environment variable only, and never prints, logs or stores it. It writes only to the
Mirror's database (mirror.notion_database_id), never touches a page with Pending checked (ADR 0001), and
lists pages that aren't in the plan instead of trashing them, unless the learner named them with --trash.

Setting PRACTICE_LOG_NOTION_FAKE to a JSON file of canned responses replaces the network: every request
is printed instead of sent. The Seam 1 cases use it.
"""

import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from practice_log.mirror import KEY, PlanError, build_plan, only_changed, page_hash, read_state, STATE_FILE
from practice_log.readme import plural
from practice_log.workspace import CONFIG_FILE

API = "https://api.notion.com"
NOTION_VERSION = "2026-03-11"
TOKEN_VARIABLE = "NOTION_TOKEN"
FAKE_VARIABLE = "PRACTICE_LOG_NOTION_FAKE"
TEXT_MAX = 2000
CHILDREN_MAX = 100
# The properties a push can't do without: the key it matches pages by, and the mark that protects pending pages.
REQUIRED = {"Problem ID": "rich_text", "Pending": "checkbox"}
LANGUAGES = {
    "bash": "bash", "c": "c", "c#": "c#", "c++": "c++", "cpp": "c++", "csharp": "c#", "go": "go",
    "java": "java", "javascript": "javascript", "js": "javascript", "json": "json", "kotlin": "kotlin",
    "markdown": "markdown", "md": "markdown", "python": "python", "py": "python", "ruby": "ruby",
    "rust": "rust", "shell": "shell", "sh": "shell", "sql": "sql", "swift": "swift",
    "typescript": "typescript", "ts": "typescript",
}


class PushError(RuntimeError):
    pass


# --- HTTP: the real API, or a fake that prints every request ---


class NotionApi:
    # Notion allows about three requests a second; a full push can make thousands.
    PACE = 0.35
    RATE_LIMIT_RETRIES = 8
    SERVER_ERROR_RETRIES = 3

    def __init__(self, token):
        self.token = token
        self.last = 0.0

    def call(self, method, path, body=None):
        data = None if body is None else json.dumps(body).encode("utf-8")
        limited = failed = 0
        while True:
            wait = self.last + self.PACE - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self.last = time.monotonic()
            request = urllib.request.Request(API + path, data=data, method=method)
            request.add_header("Authorization", "Bearer " + self.token)
            request.add_header("Notion-Version", NOTION_VERSION)
            request.add_header("Content-Type", "application/json")
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    return json.loads(response.read().decode("utf-8") or "{}")
            except urllib.error.HTTPError as error:
                if error.code == 429 and limited < self.RATE_LIMIT_RETRIES:
                    limited += 1
                    time.sleep(retry_after(error.headers.get("Retry-After"), limited))
                    continue
                # A 5xx can come after Notion did the work, so only requests that are safe to repeat are retried.
                if error.code in (500, 502, 503, 504) and repeatable(method, path) and failed < self.SERVER_ERROR_RETRIES:
                    failed += 1
                    time.sleep(2 ** failed)
                    continue
                raise PushError(f"Notion answered {error.code} to {method} {path}{notion_message(error)}") from None
            except urllib.error.URLError as error:
                raise PushError(f"could not reach Notion ({error.reason}) at {method} {path}") from None
            except (OSError, http.client.HTTPException, ValueError) as error:
                raise PushError(f"{method} {path} failed ({type(error).__name__}); nothing after it was written") from None


def repeatable(method, path):
    """GET, DELETE and property updates give the same result when sent twice; creating or appending doesn't."""
    if method in ("GET", "DELETE"):
        return True
    return method == "PATCH" and not path.endswith("/children")


def retry_after(value, attempt):
    try:
        return min(float(value), 60.0)
    except (TypeError, ValueError):
        return float(min(2 ** attempt, 30))


def notion_message(error):
    try:
        message = json.loads(error.read().decode("utf-8")).get("message", "")
    except (OSError, ValueError, AttributeError):
        message = ""
    return f": {message}" if message else ""


class FakeApi:
    """Canned responses keyed by "METHOD path"; a write with no canned response gets a new fake id.

    A response {"__error": 500} makes that request fail the way Notion's error would, and
    {"__sequence": [first, second]} answers successive calls in turn (for pagination).
    """

    def __init__(self, path):
        self.responses = json.loads(Path(path).read_text(encoding="utf-8"))
        self.count = 0
        print(
            f"notion: fake API from {FAKE_VARIABLE}; each request carries Notion-Version: {NOTION_VERSION}"
            f" and Authorization: Bearer <{TOKEN_VARIABLE}>"
        )

    def call(self, method, path, body=None):
        print(f"\n{method} {path}")
        if body is not None:
            print(json.dumps(body, ensure_ascii=False, indent=2))
        key = f"{method} {path}"
        if key in self.responses:
            response = self.responses[key]
            if isinstance(response, dict) and "__sequence" in response:
                # Successive calls get successive responses, the last one repeating.
                sequence = response["__sequence"]
                response = sequence.pop(0) if len(sequence) > 1 else sequence[0]
            if isinstance(response, dict) and "__error" in response:
                raise PushError(f"Notion answered {response['__error']} to {method} {path}")
            return response
        if method == "GET" or path.endswith("/query"):
            raise PushError(f"fake API: no response for {key}")
        self.count += 1
        return {"id": f"fake-{self.count:04d}"}


TOKEN_SHAPE = re.compile(r"[A-Za-z0-9_-]+")


def open_api():
    fake = os.environ.get(FAKE_VARIABLE)
    if fake:
        return FakeApi(fake)
    token = os.environ.get(TOKEN_VARIABLE, "").strip()
    if not token:
        raise PushError(
            f"mirror-push: set {TOKEN_VARIABLE} to an internal integration's token (create one at"
            " https://www.notion.so/my-integrations, then share the Mirror's database, or the page above it,"
            " with that integration)"
        )
    if not TOKEN_SHAPE.fullmatch(token):
        # Never repeat the value: an error message is the one place it could leak.
        raise PushError(
            f"mirror-push: {TOKEN_VARIABLE} holds characters an integration token never has (such as a line break"
            " or quote); set it again to just the secret Notion shows"
        )
    return NotionApi(token)


# --- Markdown to Notion blocks: only what Mirror page bodies hold ---

INLINE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)|`([^`]+)`")


def rich_text(text):
    """Plain text with Markdown links and inline code, split into Notion's 2000-character pieces."""
    parts, position = [], 0
    for match in INLINE.finditer(text):
        if match.start() > position:
            parts.append((text[position:match.start()], None, False))
        if match.group(1) is not None:
            parts.append((match.group(1), match.group(2), False))
        else:
            parts.append((match.group(3), None, True))
        position = match.end()
    if position < len(text):
        parts.append((text[position:], None, False))
    result = []
    for content, link, code in parts:
        for start in range(0, len(content), TEXT_MAX):
            piece = {"type": "text", "text": {"content": content[start:start + TEXT_MAX]}}
            if link:
                piece["text"]["link"] = {"url": link}
            if code:
                piece["annotations"] = {"code": True}
            result.append(piece)
    return result


def block(kind, text):
    return {"object": "block", "type": kind, kind: {"rich_text": rich_text(text)}}


def to_blocks(markdown):
    """Blocks for a Mirror page body: quotes, ## and ### headings, bullets, fenced code and paragraphs."""
    blocks, lines, index = [], markdown.split("\n"), 0
    while index < len(lines):
        line = lines[index]
        fence = re.match(r"^(`{3,}|~{3,})\s*(\S*)", line)
        if fence:
            marker, language, body = fence.group(1), fence.group(2).lower(), []
            index += 1
            while index < len(lines) and not lines[index].startswith(marker):
                body.append(lines[index])
                index += 1
            code = {"rich_text": rich_text_plain("\n".join(body)), "language": LANGUAGES.get(language, "plain text")}
            blocks.append({"object": "block", "type": "code", "code": code})
        elif line.startswith("> "):
            blocks.append(block("quote", line[2:]))
        elif line.startswith("### "):
            blocks.append(block("heading_3", line[4:]))
        elif line.startswith("## "):
            blocks.append(block("heading_2", line[3:]))
        elif line.startswith("- "):
            blocks.append(block("bulleted_list_item", line[2:]))
        elif line.strip():
            blocks.append(block("paragraph", line))
        index += 1
    return blocks


def rich_text_plain(text):
    return [{"type": "text", "text": {"content": text[start:start + TEXT_MAX]}} for start in range(0, len(text), TEXT_MAX)] or []


# --- Plan values to Notion property values ---


def property_value(kind, value):
    if kind == "title":
        return {"title": rich_text_plain(value)}
    if kind == "text":
        return {"rich_text": rich_text_plain(value or "")}
    if kind == "select":
        return {"select": {"name": value} if value else None}
    if kind == "multi_select":
        return {"multi_select": [{"name": name} for name in value]}
    if kind == "checkbox":
        return {"checkbox": bool(value)}
    if kind == "number":
        return {"number": value}
    if kind == "date":
        return {"date": {"start": value} if value else None}
    if kind == "url":
        return {"url": value or None}
    raise ValueError(kind)


def schema(prop):
    kind = "rich_text" if prop["type"] == "text" else prop["type"]
    config = {}
    if "options" in prop:
        config = {"options": [dict(option) for option in prop["options"]]}
    return {kind: config}


def page_properties(plan, page):
    return {
        prop["name"]: property_value(prop["type"], page["properties"][prop["name"]])
        for prop in plan["database"]["properties"]
    }


def plain(value):
    """The text of a property read back from Notion."""
    kind = value.get("type")
    if kind in ("rich_text", "title"):
        return "".join(part.get("plain_text", part.get("text", {}).get("content", "")) for part in value[kind])
    return value.get(kind)


# --- The push ---


def run(root, changed=False, parent=None, trash=()):
    try:
        api = open_api()
        return push(api, root, changed, parent, list(trash))
    except (PlanError, PushError) as error:
        message = str(error).replace("mirror-plan:", "mirror-push:")
        for line in message.splitlines():
            print(line if line.startswith("mirror-push") else "mirror-push: " + line, file=sys.stderr)
        return 1


def push(api, root, changed, parent, trash):
    full_plan = build_plan(root)
    state = read_state(root)
    plan = only_changed(full_plan, state) if changed else full_plan
    database_id = full_plan["database"]["id"]
    if database_id is None:
        if not parent:
            raise PushError(
                "mirror-push: no Mirror yet; name the Notion page to create it in with --parent <page link or id>,"
                " a page shared with the integration"
            )
        database_id, source_id = create_database(api, root, full_plan, page_id(parent))
        state, created_now = None, True
    else:
        source_id, created_now = check_database(api, database_id, full_plan), False
    ensure_views(api, database_id, source_id, full_plan, created_now)

    pending, by_id, duplicates = read_pages(api, source_id)
    recorded = dict(state["pages"]) if state and state.get("notion_database_id") == database_id else {}
    created = updated = 0
    for page in plan["pages"]:
        problem_id = page["properties"][KEY]
        existing = by_id.get(problem_id)
        properties = page_properties(full_plan, page)
        blocks = to_blocks(page["body"])
        # Forget the page before touching it: when a write fails halfway, the next --changed push repairs it.
        if recorded.pop(problem_id, None) is not None:
            write_state(root, database_id, recorded)
        if existing:
            api.call("PATCH", f"/v1/pages/{existing}", {"properties": properties})
            replace_children(api, existing, blocks)
            updated += 1
        else:
            response = api.call("POST", "/v1/pages", {
                "parent": {"type": "data_source_id", "data_source_id": source_id},
                "properties": properties,
                "children": blocks[:CHILDREN_MAX],
            })
            append_children(api, response["id"], blocks[CHILDREN_MAX:])
            created += 1
        recorded[problem_id] = page_hash(page)
        write_state(root, database_id, recorded)

    in_plan = {page["properties"][KEY] for page in full_plan["pages"]}
    not_in_plan = sorted({problem_id for problem_id in by_id if problem_id not in in_plan})
    trashed = []
    for problem_id in trash:
        if problem_id in in_plan or problem_id not in by_id:
            print(f"mirror-push: --trash {problem_id}: no page outside the plan has that Problem ID; nothing trashed", file=sys.stderr)
            continue
        api.call("PATCH", f"/v1/pages/{by_id[problem_id]}", {"in_trash": True})
        recorded.pop(problem_id, None)
        trashed.append(problem_id)
    write_state(root, database_id, recorded)

    summary = f"mirror-push: created {plural(created, 'page')}, updated {updated}"
    if changed:
        summary += f", left out {len(plan['changes']['unchanged'])} unchanged"
    if trashed:
        summary += f", moved {len(trashed)} to Notion's trash"
    print(summary)
    if pending:
        print(f"mirror-push: left {plural(len(pending), 'pending page')} alone; Import brings them into the Practice Log")
    leftover = [problem_id for problem_id in not_in_plan if problem_id not in trashed]
    if leftover or duplicates:
        print("mirror-push: not in the plan, so left as they are; ask the learner before moving them to Notion's trash"
              " (mirror-push --trash <Problem ID>):")
        for problem_id in leftover:
            print(f"- {problem_id or '(no Problem ID)'}")
        for problem_id in duplicates:
            print(f"- {problem_id} (a second page for one Problem ID; trash it in Notion)")
    return 0


def page_id(text):
    match = re.search(r"([0-9a-f]{32})(?:[?#]|$)|([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", text.strip())
    if not match:
        raise PushError(f"mirror-push: --parent '{text}' is not a Notion page link or id")
    return (match.group(1) or match.group(2)).replace("-", "")


def create_database(api, root, plan, parent):
    database = plan["database"]
    response = api.call("POST", "/v1/databases", {
        "parent": {"type": "page_id", "page_id": parent},
        "title": rich_text_plain(database["title"]),
        "description": rich_text_plain(database["description"]),
        "is_inline": False,
        "initial_data_source": {"properties": {prop["name"]: schema(prop) for prop in database["properties"]}},
    })
    database_id = response["id"]
    # Stored straight away, so a failed push never leaves a second database behind.
    config_file = root / CONFIG_FILE
    config = json.loads(config_file.read_text(encoding="utf-8-sig"))
    config.setdefault("mirror", {})["notion_database_id"] = database_id
    config_file.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"mirror-push: created the Mirror database {database_id} and stored its id in {CONFIG_FILE}")
    sources = response.get("data_sources") or []
    if not sources:
        sources = api.call("GET", f"/v1/databases/{database_id}").get("data_sources") or []
    return database_id, sources[0]["id"]


def check_database(api, database_id, plan):
    database = api.call("GET", f"/v1/databases/{database_id}")
    sources = database.get("data_sources") or []
    if not sources:
        raise PushError(f"mirror-push: database {database_id} has no data source")
    source_id = sources[0]["id"]
    source = api.call("GET", f"/v1/data_sources/{source_id}")
    existing = source.get("properties", {})
    missing = [name for name, kind in REQUIRED.items() if existing.get(name, {}).get("type") != kind]
    if missing:
        raise PushError(
            f"mirror-push: the Mirror database has no {' or '.join(repr(name) for name in missing)} property of the"
            " right type (Problem ID is text, Pending a checkbox), so nothing was pushed; rename or change it back"
            " in Notion, then push again"
        )
    changes = {}
    for prop in plan["database"]["properties"]:
        current = existing.get(prop["name"])
        if current is None:
            changes[prop["name"]] = schema(prop)
            continue
        if "options" not in prop:
            continue
        kind = current.get("type")
        have = current.get(kind, {}).get("options", [])
        names = {option["name"] for option in have}
        wanted = [option for option in prop["options"] if option["name"] not in names]
        if wanted:
            # Every existing option keeps its colour; options left out would be removed.
            kept = [{"name": option["name"], "color": option.get("color", "default")} for option in have]
            changes[prop["name"]] = {kind: {"options": kept + [dict(option) for option in wanted]}}
    if changes:
        api.call("PATCH", f"/v1/data_sources/{source_id}", {"properties": changes})
    return source_id


def ensure_views(api, database_id, source_id, plan, created_now=False):
    """Add the plan's views the database lacks, by name; never change one that exists, except a new database's default."""
    listed = api.call("GET", f"/v1/views?database_id={database_id}").get("results", [])
    views = [api.call("GET", f"/v1/views/{view['id']}") for view in listed]
    names = {view.get("name") for view in views}
    wanted = [view for view in plan["database"]["views"] if view["name"] not in names]
    if not wanted:
        return
    ids = {name: prop.get("id", name) for name, prop in
           api.call("GET", f"/v1/data_sources/{source_id}").get("properties", {}).items()}
    # A database the push just created has one default table view ("Default view"): make it the plan's first view.
    reuse = views[0]["id"] if created_now and len(views) == 1 and wanted[0]["type"] == "table" else None
    for view in wanted:
        body = view_body(view, ids)
        if reuse:
            api.call("PATCH", f"/v1/views/{reuse}", body)
            reuse = None
        else:
            api.call("POST", "/v1/views", {"database_id": database_id, "data_source_id": source_id, **body})


def view_body(view, ids):
    body = {"name": view["name"], "type": view["type"]}
    if view["type"] == "table":
        shown = view["show"]
        hidden = [name for name in ids if name not in shown]
        body["sorts"] = view.get("sort", [])
        body["configuration"] = {
            "type": "table",
            "properties": [{"property_id": ids[name], "visible": True} for name in shown if name in ids]
            + [{"property_id": ids[name], "visible": False} for name in hidden],
        }
    elif view["type"] == "calendar":
        body["configuration"] = {"type": "calendar", "date_property_id": ids.get(view["calendar_by"], view["calendar_by"])}
    return body


def read_pages(api, source_id):
    """Pending page ids, the other pages by Problem ID, and Problem IDs with more than one such page."""
    pending, by_id, duplicates, cursor = [], {}, [], None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        response = api.call("POST", f"/v1/data_sources/{source_id}/query", body)
        for page in response.get("results", []):
            properties = page.get("properties", {})
            if properties.get("Pending", {}).get("checkbox"):
                pending.append(page["id"])
                continue
            problem_id = plain(properties.get(KEY, {"type": "rich_text", "rich_text": []})) or ""
            if problem_id in by_id:
                duplicates.append(problem_id)
            else:
                by_id[problem_id] = page["id"]
        cursor = response.get("next_cursor")
        if not response.get("has_more") or not cursor:
            return pending, by_id, sorted(set(duplicates))


def replace_children(api, page, blocks):
    cursor, old = None, []
    while True:
        query = f"?page_size=100&start_cursor={cursor}" if cursor else "?page_size=100"
        response = api.call("GET", f"/v1/blocks/{page}/children{query}")
        # A subpage or database inside the page is the learner's own; never delete it.
        old += [child["id"] for child in response.get("results", [])
                if child.get("type") not in ("child_page", "child_database")]
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")
        if not cursor:
            break
    for child in old:
        api.call("DELETE", f"/v1/blocks/{child}")
    append_children(api, page, blocks)


def append_children(api, page, blocks):
    for start in range(0, len(blocks), CHILDREN_MAX):
        api.call("PATCH", f"/v1/blocks/{page}/children", {"children": blocks[start:start + CHILDREN_MAX]})


def write_state(root, database_id, pages):
    text = json.dumps(
        {"version": 1, "notion_database_id": database_id, "pages": dict(sorted(pages.items()))},
        ensure_ascii=False,
        indent=2,
    )
    (root / STATE_FILE).write_text(text + "\n", encoding="utf-8", newline="\n")


# --- mirror-pending: Import's pending check through the API ---


def pending(root, trash=()):
    """`mirror-pending`: print every pending page in the Mirror as Markdown, or trash the named ones."""
    try:
        api = open_api()
        database_id = build_plan(root)["database"]["id"]
        if database_id is None:
            print("mirror-pending: no Mirror yet (mirror.notion_database_id is empty), so no pending pages")
            return 0
        sources = api.call("GET", f"/v1/databases/{database_id}").get("data_sources") or []
        if not sources:
            raise PushError(f"mirror-pending: database {database_id} has no data source")
        source_id = sources[0]["id"]
        pages, cursor = [], None
        while True:
            body = {"page_size": 100, "filter": {"property": "Pending", "checkbox": {"equals": True}}}
            if cursor:
                body["start_cursor"] = cursor
            response = api.call("POST", f"/v1/data_sources/{source_id}/query", body)
            pages += response.get("results", [])
            cursor = response.get("next_cursor")
            if not response.get("has_more") or not cursor:
                break
        # Check Pending here too, not only through Notion's filter: only a pending page may be trashed.
        pages = [page for page in pages if page.get("properties", {}).get("Pending", {}).get("checkbox") is True]
        ids = {page["id"].replace("-", ""): page for page in pages}
        if trash:
            for page in trash:
                key = page.replace("-", "")
                if key not in ids:
                    print(f"mirror-pending: {page} is not a pending page of the Mirror; nothing trashed", file=sys.stderr)
                    continue
                api.call("PATCH", f"/v1/pages/{ids[key]['id']}", {"in_trash": True})
                print(f"mirror-pending: moved {page} to Notion's trash")
            return 0
        print(f"mirror-pending: {plural(len(pages), 'pending page')}")
        for page in pages:
            problem_id = plain(page.get("properties", {}).get(KEY, {"type": "rich_text", "rich_text": []})) or ""
            print(f"\n## Pending page {page['id']} ({problem_id or 'no Problem ID'})\n")
            print(to_markdown(read_children(api, page["id"])))
        return 0
    except (PlanError, PushError) as error:
        for line in str(error).replace("mirror-plan:", "mirror-pending:").replace("mirror-push:", "mirror-pending:").splitlines():
            print(line, file=sys.stderr)
        return 1


def read_children(api, page):
    cursor, blocks = None, []
    while True:
        query = f"?page_size=100&start_cursor={cursor}" if cursor else "?page_size=100"
        response = api.call("GET", f"/v1/blocks/{page}/children{query}")
        blocks += response.get("results", [])
        cursor = response.get("next_cursor")
        if not response.get("has_more") or not cursor:
            return blocks


def markdown_text(parts):
    out = []
    for part in parts:
        text = part.get("plain_text", part.get("text", {}).get("content", ""))
        link = (part.get("text") or {}).get("link") or ({"url": part["href"]} if part.get("href") else None)
        if (part.get("annotations") or {}).get("code"):
            text = f"`{text}`"
        out.append(f"[{text}]({link['url']})" if link else text)
    return "".join(out)


def to_markdown(blocks):
    """The page's content as Markdown, the inverse of to_blocks for the blocks a pending page holds."""
    prefixes = {"quote": "> ", "heading_1": "# ", "heading_2": "## ", "heading_3": "### ",
                "bulleted_list_item": "- ", "numbered_list_item": "1. ", "paragraph": ""}
    lines = []
    for item in blocks:
        kind = item.get("type")
        content = item.get(kind, {})
        if kind == "code":
            code = "".join(part.get("plain_text", part.get("text", {}).get("content", "")) for part in content.get("rich_text", []))
            language = content.get("language", "")
            fence = "`" * max(3, max((len(run) for run in re.findall(r"`+", code)), default=0) + 1)
            lines.append(f"{fence}{'' if language == 'plain text' else language}\n{code}\n{fence}")
        elif kind in prefixes:
            lines.append(prefixes[kind] + markdown_text(content.get("rich_text", [])))
        elif kind == "divider":
            lines.append("---")
    return "\n\n".join(lines)
