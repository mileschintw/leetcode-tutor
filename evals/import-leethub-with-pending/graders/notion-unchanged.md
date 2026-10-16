---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(?:create-pages|create-database|update-page|move-pages|delete-pages)"'
match: not_contains
---

Before the learner confirms, nothing in Notion changes: the pending page is trashed only after the write.
