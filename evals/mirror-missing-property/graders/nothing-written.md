---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(?:create-pages|create-database|update-page|update-data-source|move-pages|delete-pages)"'
match: not_contains
---

Without Problem ID no page can be matched, so the push writes nothing: no page, no option change, no new database.
