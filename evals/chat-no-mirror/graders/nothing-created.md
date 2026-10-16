---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(?:create-database|create-pages|update-page|move-pages|delete-pages)"'
match: not_contains
---

With no Mirror to write to, nothing is created or changed in Notion: a Mirror database is only made by a push from the Practice Workspace.
