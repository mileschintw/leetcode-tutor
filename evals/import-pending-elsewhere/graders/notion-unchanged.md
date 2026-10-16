---
type: regex
target: mock_calls
pattern: '"tool":\s*"(?:[\w-]+__)?notion-(?:create-pages|create-database|update-page|move-pages|delete-pages)"'
match: not_contains
---

The page in the other database is reported, not imported or trashed: the learner hasn't asked for it yet.
