# Practice Log schema

The format of the learner's Practice Log inside their Practice Workspace. `validate` (see [practice-workspace.md](practice-workspace.md)) checks the fields, values and code files below; follow the naming and heading conventions yourself.

## Contents

- Workspace layout
- Workspace config
- Problem ID
- Notes file
- Problem fields
- Attempts
- Example

## Workspace layout

```text
practice-log.json              workspace config; marks the folder as a Practice Workspace
README.md                      index of the Practice Log
problems/<source>/<slug>/      one folder per Problem
  notes.md                     Problem fields, Key Takeaway, Attempt log
  <date>-<approach>.<ext>      one code file per Attempt
review-sheets/                 saved Review Sheets, <date>-<goal slug>.md (see review-sheet.md)
```

Other files in a Problem's folder, such as a self-authored Problem's test harness, are the learner's own and stay as they are.

## Workspace config

`practice-log.json`, which `init` creates:

```json
{
  "version": 1,
  "mirror": {
    "notion_database_id": null,
    "repository": "https://github.com/<owner>/<repo>"
  }
}
```

- `version`: always `1`.
- `mirror.notion_database_id`: the Notion database the Mirror created and owns; `null` until the first push (the `practice-log-mirror` skill sets it).
- `mirror.repository`: the workspace's GitHub repository, which Mirror pages link to. Optional; `init` leaves it out, and the `practice-log-mirror` skill sets it from the `origin` remote.

## Problem ID

`<source>:<slug>`, both parts lowercase ASCII letters, digits and single hyphens. The Problem's folder is `problems/<source>/<slug>/`.

- **LeetCode:** `leetcode:<slug>`, the slug from the problem URL (`leetcode.com/problems/two-sum/` → `leetcode:two-sum`).
- **NeetCode:** `neetcode:<slug>`, the slug from the NeetCode URL, for NeetCode's own Problems. A Problem NeetCode links to on LeetCode is a `leetcode:` Problem.
- **Custom:** `custom:<slug>` for the learner's own exercises; choose a short slug from the title (`custom:lru-cache`).

The same exercise on two sites is two Problem IDs. Before creating a folder, look for an existing one with the same ID, and add the Attempt there.

## Notes file

`notes.md` has YAML frontmatter holding the Problem fields, then two sections in this order:

1. `## Key Takeaway`: the Problem's Key Takeaway, updated when a later Attempt sharpens it.
2. `## Attempts`: the Attempt log, oldest first, one `###` heading per Attempt.

## Problem fields

Flat frontmatter, Obsidian-compatible. Lists may be written `[a, b]` or as `- item` lines.

| Field | Required | Value |
| --- | --- | --- |
| `id` | yes | the Problem ID |
| `title` | yes | the Problem's title as its source writes it |
| `difficulty` | no | `easy`, `medium` or `hard`; leave empty when the source has none |
| `tags` | no | list of algorithm and data-structure tags only (`array`, `hash-table`), lowercase and hyphenated |
| `link` | no | the Problem's URL; empty for a custom Problem without one |
| `lists` | no | list of Problem List names (`Grind 75`, `NeetCode 150`); names differing only in case are one list |
| `need_review` | yes | `true` or `false` |
| `need_review_reason` | when `need_review` is `true` | why it was last set, in one line; empty when `need_review` is `false` |

When the tutor sets and clears Need Review is in [need-review.md](need-review.md).

## Attempts

Each Attempt is a `### <date> <approach>` heading followed by unindented `- key: value` lines, one line per value. Indented bullets and fenced code blocks after them are the learner's own notes, not fields:

| Key | Required | Value |
| --- | --- | --- |
| `date` | yes | `YYYY-MM-DD`, the day of the Session |
| `mode` | yes | `session` (the full Socratic flow) or `recap` (Recap Mode) |
| `outcome` | yes | `solved-alone`, `solved-with-hints` or `saw-solution` |
| `approach` | yes | a short name for the approach (`hash map`, `two pointers`) |
| `mistakes` | no | what went wrong during the Session, in one line; `none` when nothing did. Leave the line out when it isn't known, as for an imported record that doesn't say |
| `language` | yes | the code's language, lowercase (`python`, `cpp`, `java`) |
| `code` | yes | the code file's name in the Problem's folder (no subfolders) |
| `origin` | no | where an Attempt came from when it was not written in a Session in the Practice Workspace (`notion`, `leethub`; `mirror-pending` for a pending page in the Mirror and `chat` for a pasted Attempt block, see [chat-platforms.md](chat-platforms.md)) |

Outcomes:

- `solved-alone`: the learner reached a working solution with no hints beyond the First Response.
- `solved-with-hints`: the learner wrote the solution after hints, corrections or pseudocode review.
- `saw-solution`: the learner saw the solution (asked for it, a skeleton, or a jump to the conclusion) before solving it.

A `recap` Attempt's outcome is judged by the learner's recall of the Key Takeaway instead (see [modes.md](modes.md)).

The code file is named `<date>-<approach slug>.<ext>`, for example `2026-10-15-hash-map.py`. If that name is taken, add `-2`, `-3` and so on before the extension.

Nothing else is recorded: the number of Attempts comes from the log, and last-updated times come from git.

## Example

`problems/leetcode/two-sum/notes.md`:

```markdown
---
id: leetcode:two-sum
title: Two Sum
difficulty: easy
tags: [array, hash-table]
link: https://leetcode.com/problems/two-sum/
lists: [Grind 75, NeetCode 150]
need_review: false
need_review_reason:
---

## Key Takeaway

Use a hash map to store each value's index as you iterate, and look up `target - value` before inserting, for O(1) complement checks.

## Attempts

### 2026-10-15 hash map

- date: 2026-10-15
- mode: session
- outcome: solved-with-hints
- approach: hash map
- mistakes: Returned the values instead of their indices; inserted before checking, so `[3, 3]` matched an element with itself.
- language: python
- code: 2026-10-15-hash-map.py
```
