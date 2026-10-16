---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(?:create-pages|create-database|update-page|move-pages|delete-pages)"'
match: not_contains
---

Nothing changes in Notion: the already-imported pending page is only offered for the trash, not trashed unasked.
